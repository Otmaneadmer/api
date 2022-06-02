<template>
  <v-container fluid>
    <div class="tables-basic">
      <h1 class="page-title mt-10 mb-6">Gestion des Amphitheatres</h1>
      <v-alert v-if="errors.length > 0" border="left" close-text="Fermer" color="red accent-4" dark dismissible>
        <ul>
          <li v-for="(err, i) in errors" :key="i"> {{ e }}</li>
        </ul>
      </v-alert>
      <v-data-table :headers="headers" :items="amphitheatres" sort-by="titre" class="elevation-1">
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Liste des Amphitheatres</v-toolbar-title>
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
                          <v-text-field v-model="editedItem.nom" label="Nom Amphitheatre" :rules="nomRules">
                          </v-text-field>
                        </v-col>

                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.numero" :rules="numeroRules" label="Numero">
                          </v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.capacite" :rules="capaciteRules"
                            label="Capacité"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.cout" :rules="coutRules" label="Cout">
                          </v-text-field>
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
      { text: "numero", value: "numero" },
      { text: "capacite", value: "capacite" },
      { text: "cout", value: "cout" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    amphitheatres: [],
    editedIndex: -1,
    deletedID: -1,
    nomRules: [
        v => !!v || 'Le nom est Obligatoire',

      ],
        numeroRules: [
        v => !!v || 'Le numero est Obligatoire',
        v => (v && Number.isInteger(Number(v))) || 'Le numero doit être un nombre.',
      ],
       capaciteRules: [
        v => !!v || 'La capacite est Obligatoire',
        v => (v && Number.isInteger(Number(v))) || 'La capacite doit être un nombre.',
      ],
       coutRules: [
        v => !!v || 'Le cout est Obligatoire',
        v => (v && Number.isInteger(Number(v))) || 'Le cout doit être un nombre.',
      ],
    editedItem: {
      nom: "",
      
      numero: "",
    
      capacite: "",
     
      cout: "",
     
    },
     valid: true,
    defaultItem: {
      nom: "",
      numero: "",
      capacite: "",
      cout: "",
    },
    menu1: false,
    menu2: false,
    errors: [],
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1
        ? "Ajouter Amphitheatre"
        : "Modifier Amphitheatre";
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
      let url = "amphitheatres/";
      axios
        .get(url)
        .then((response) => {
          console.log(response);
          this.amphitheatres = response.data;
        })
        .catch((e) => {
          this.errors.push(e);
          console.log(e);
        });
    },

    editItem(item) {
      this.editedIndex = this.amphitheatres.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.deletedID = item.id;

      //this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      let url = "amphitheatres/";
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


        let url = "amphitheatres/";
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

          // this.amphitheatres.push(this.editedItem);
        }
        this.close();

      }
    },
    showMessage(msg) {
      this.$toast.success(msg);
    },
    showItem(item) {
      this.$router.push({ name: 'DetailsAmphitheatre', params: { id: item.id } });
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
