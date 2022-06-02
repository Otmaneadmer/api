<template>
  <v-container fluid>
    <div class="tables-basic">
      <h1 class="page-title mt-10 mb-6">Gestion des Conférences</h1>

      <v-data-table
        :headers="headers"
        :items="desserts"
        sort-by="titre"
        class="elevation-1"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Liste des Conférences</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialog" max-width="1000px">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  dark
                  class="mb-2"
                  v-bind="attrs"
                  v-on="on"
                >
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
                    <v-row>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field
                          v-model="editedItem.titre"
                          label="Titre Conférence"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-menu
                          ref="menu1"
                          v-model="menu1"
                          :close-on-content-click="false"
                          :return-value.sync="date"
                          transition="scale-transition"
                          offset-y
                          min-width="auto"
                        >
                          <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                              v-model="editedItem.date_debut"
                              label="Date Debut"
                              prepend-icon="mdi-calendar"
                              readonly
                              v-bind="attrs"
                              v-on="on"
                            ></v-text-field>
                          </template>
                          <v-date-picker
                            v-model="editedItem.date_debut"
                            no-title
                            scrollable
                          >
                            <v-spacer></v-spacer>
                            <v-btn text color="primary" @click="menu1 = false">
                              Annuler
                            </v-btn>
                            <v-btn
                              text
                              color="primary"
                              @click="$refs.menu1.save(date)"
                            >
                              Valider
                            </v-btn>
                          </v-date-picker>
                        </v-menu>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-menu
                          ref="menu2"
                          v-model="menu2"
                          :close-on-content-click="false"
                          :return-value.sync="date"
                          transition="scale-transition"
                          offset-y
                          min-width="auto"
                        >
                          <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                              v-model="editedItem.date_fin"
                              label="Date Fin"
                              prepend-icon="mdi-calendar"
                              readonly
                              v-bind="attrs"
                              v-on="on"
                            ></v-text-field>
                          </template>
                          <v-date-picker
                            v-model="editedItem.date_fin"
                            no-title
                            scrollable
                          >
                            <v-spacer></v-spacer>
                            <v-btn text color="primary" @click="menu2 = false">
                              Annuler
                            </v-btn>
                            <v-btn
                              text
                              color="primary"
                              @click="$refs.menu2.save(date)"
                            >
                              Valider
                            </v-btn>
                          </v-date-picker>
                        </v-menu>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field
                          v-model="editedItem.frais"
                          label="Frais"
                        ></v-text-field>
                      </v-col>
                    </v-row>
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
                <v-card-title class="text-h7 text-center"
                  >voulez-vous vraiment supprimer cet élément ?</v-card-title
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="closeDelete"
                    >Annuler</v-btn
                  >
                  <v-btn color="red darken-1" text @click="deleteItemConfirm"
                    >Oui, Supprimer</v-btn
                  >
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
                
                   <v-icon >
                      mdi-cog-outline
                    </v-icon>
                      Actions 
                </v-btn>
              </template>
              <v-list>
                 <v-list-item @click="showItem(item)">
                  <v-list-item-title
                    >Consulter
                    <v-icon >
                      mdi-eye
                    </v-icon></v-list-item-title
                  >
                </v-list-item>
                <v-list-item @click="editItem(item)">
                  <v-list-item-title
                    >Modifier
                    <v-icon >
                      mdi-pencil
                    </v-icon></v-list-item-title
                  >
                </v-list-item>
                <v-list-item @click="deleteItem(item)"> 
                  <v-list-item-title
                    >Supprimer
                    <v-icon  >
                      mdi-delete
                    </v-icon></v-list-item-title
                  >
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
      { text: "Titre", value: "titre" },
      { text: "Date Debut", value: "date_debut" },
      { text: "Date Fin", value: "date_fin" },
      { text: "Frais", value: "frais" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    desserts: [],
    editedIndex: -1,
    editedItem: {
      titre: "",
      date_debut: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      date_fin: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      frais: 0,
      protein: 0,
    },
    defaultItem: {
      titre: "",
      date_debut: "",
      date_fin: "",
      Frais: 0,
    },
    menu1: false,
    menu2: false,
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1
        ? "Ajouter Conférence"
        : "Modifier Conférence";
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
      this.desserts = [
        {
          titre: "Frozen Yogurt",
          date_debut: 159,
          date_fin: 6.0,
          frais: 24,
          protein: 4.0,
        },
        {
          titre: "Ice cream sandwich",
          date_debut: 237,
          date_fin: 9.0,
          frais: 37,
          protein: 4.3,
        },
        {
          titre: "Eclair",
          date_debut: 262,
          date_fin: 16.0,
          frais: 23,
          protein: 6.0,
        },
        {
          titre: "Cupcake",
          date_debut: 305,
          date_fin: 3.7,
          frais: 67,
          protein: 4.3,
        },
        {
          titre: "Gingerbread",
          date_debut: 356,
          date_fin: 16.0,
          frais: 49,
          protein: 3.9,
        },
        {
          titre: "Jelly bean",
          date_debut: 375,
          date_fin: 0.0,
          frais: 94,
          protein: 0.0,
        },
        {
          titre: "Lollipop",
          date_debut: 392,
          date_fin: 0.2,
          frais: 98,
          protein: 0,
        },
        {
          titre: "Honeycomb",
          date_debut: 408,
          date_fin: 3.2,
          frais: 87,
          protein: 6.5,
        },
        {
          titre: "Donut",
          date_debut: 452,
          date_fin: 25.0,
          frais: 51,
          protein: 4.9,
        },
        {
          titre: "KitKat",
          date_debut: 518,
          date_fin: 26.0,
          frais: 65,
          protein: 7,
        },
      ];
    },

    editItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.desserts.splice(this.editedIndex, 1);
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
      if (this.editedIndex > -1) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem);
      } else {
        this.desserts.push(this.editedItem);
      }
      this.close();
    },
  },
};
</script>

<style src="./Basic.scss" lang="scss"></style>
