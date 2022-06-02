<template>
  <v-container fluid>
    <div class="tables-basic">
      <h1 class="page-title mt-10 mb-6">Gestion des Participants</h1>
      <v-alert v-if="errors.length > 0" border="left" close-text="Fermer" color="red accent-4" dark dismissible>
        <ul>
          <li v-for="(err, i) in errors" :key="i"> {{ e }}</li>
        </ul>
      </v-alert>
      <v-data-table :headers="headers" :items="participants" sort-by="titre" class="elevation-1">
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Liste des Participants</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialog" max-width="1000px">
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                  Nouveau
                  <v-icon right dark> mdi-plus </v-icon>
                </v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="text-h5">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-form ref="form" v-model="valid" lazy-validation>
                      <v-row>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.nom" label="Nom" :rules="nomRules">
                          </v-text-field>
                        </v-col>

                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.prenom" :rules="prenomRules" label="Prénom">
                          </v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.cin" :rules="cinRules" label="CIN"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.telephone" :rules="telephoneRules" label="Téléphone">
                          </v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.email" :rules="emailRules" label="Email">
                          </v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field>
                          </v-text-field>
                          <v-select :items="types" v-model="editedItem.type" :rules="typeRules"
                            label="Type Participant">

                          </v-select>
                        </v-col>
                      </v-row>
                    </v-form>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="close">
                    Annuler
                  </v-btn>
                  <v-btn color="blue darken-1" text @click="save">
                    Enregistrer
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-dialog v-model="dialogDelete" max-width="700px">
              <v-card>
                <v-card-title class="text-h7 text-center">voulez-vous vraiment supprimer cet élément ?</v-card-title>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="closeDelete">Annuler</v-btn>
                  <v-btn color="red darken-1" text @click="deleteItemConfirm">Oui, Supprimer</v-btn>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <div class="text-center">
            <v-menu offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" dark v-bind="attrs" v-on="on">
                  <v-icon> mdi-cog-outline </v-icon>
                  Actions
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="showItem(item)">
                  <v-list-item-title>Consulter <v-icon> mdi-eye </v-icon>
                  </v-list-item-title>
                </v-list-item>
                <v-list-item @click="editItem(item)">
                  <v-list-item-title>Modifier <v-icon> mdi-pencil </v-icon>
                  </v-list-item-title>
                </v-list-item>
                <v-list-item @click="deleteItem(item)">
                  <v-list-item-title>Supprimer <v-icon> mdi-delete </v-icon>
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </template>
        <template v-slot:no-data>
          <v-btn color="primary" @click="initialize"> Reset </v-btn>
        </template>
      </v-data-table>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "ID",
        align: "start",
        sortable: false,
        value: "id",
      },
      { text: "nom", value: "nom" },
      { text: "prenom", value: "prenom" },
      { text: "cin", value: "cin" },
      { text: "telephone", value: "telephone" },
      { text: "email", value: "email" },
      { text: "type", value: "type" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    participants: [],
    editedIndex: -1,
    deletedID: -1,
    nomRules: [
      v => !!v || 'Le nom est Obligatoire',

    ],
    prenomRules: [
      v => !!v || 'Le prenom est Obligatoire',
    ],
    cinRules: [
      v => !!v || 'La cin est Obligatoire',
    ],
    telephoneRules: [
      v => !!v || 'Le telephone est Obligatoire',
      v => (v && Number.isInteger(Number(v))) || 'Le telephone doit être un nombre.',
    ],
    emailRules: [
      v => !!v || "L'Eamil est Obligatoire",
      v => (/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v)) || 'Entrer un Email Valide.'
    ],
    typeRules: [
      v => !!v || 'Le Type est Obligatoire',
    ],
    editedItem: {
      nom: "",

      prenom: "",

      cin: "",

      telephone: "",
      email: "",
      type: "",

    },
    valid: true,
    defaultItem: {
      nom: "",
      prenom: "",
      cin: "",
      telephone: "",
      email: "",
      type: "",
    },
    menu1: false,
    menu2: false,
    errors: [],
    types: ['Conferencier', 'Auditeur'],
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1
        ? "Ajouter Participant"
        : "Modifier Participant";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      let url = "participants/";
      axios
        .get(url)
        .then((response) => {
          console.log(response);
          this.participants = response.data;
        })
        .catch((e) => {
          this.errors.push(e);
          console.log(e);
        });
    },

    editItem(item) {
      this.editedIndex = this.participants.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.deletedID = item.id;

      //this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      let url = "participants/";
      axios
        .delete(url + this.deletedID + "/")
        .then((response) => {
          console.log(response);
          this.showMessage("Elément Supprimé avec succès.");
          this.initialize();
        })
        .catch((e) => {
          this.errors.push(e);
          console.log(e);
        });
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.validate()) {


        let url = "participants/";
        if (this.editedIndex > -1) {
          axios
            .put(url + this.editedItem.id + "/", this.editedItem)
            .then((response) => {
              console.log(response);
              this.showMessage("Elément Modifié avec succès.");
              this.initialize();
            })
            .catch((e) => {
              this.errors.push(e);
              console.log(e);
            });
        } else {
          axios
            .post(url, this.editedItem)
            .then((response) => {
              console.log(response);
              this.showMessage("Elément Enregistré avec succès.");
              this.initialize();
            })
            .catch((e) => {
              this.errors.push(e.response.data);
              console.log(e.response.data);
            });

          // this.participants.push(this.editedItem);
        }
        this.close();

      }
    },
    showMessage(msg) {
      this.$toast.success(msg);
    },
    showItem(item) {
      this.$router.push({ name: 'DetailsParticipant', params: { id: item.id } });
    },
    validate() {
      return this.$refs.form.validate()
    },

    resetValidation() {
      this.$refs.form.resetValidation()
    },
  },
};
</script>

<style src="./Basic.scss" lang="scss">
</style>
