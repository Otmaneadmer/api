<template>
  <v-container fluid>
    <div class="tables-basic">
      <h1 class="page-title mt-10 mb-6">Gestion des Amphitheatres</h1>
      <h3 class="mt-10 mb-6">Détails Amphitheatre</h3>

      <v-card class="" max-width="500">
        <v-card-text>
          <div>Nom Amphitheatre :</div>
          <p class="text-h4 text--primary">{{amphitheatre.nom}}</p>
          <div>Numéro Amphitheatre :</div>
          <p class="text-h4 text--primary">{{amphitheatre.numero}}</p>
          <div>Capacité Amphitheatre :</div>
          <p class="text-h4 text--primary">{{amphitheatre.capacite}}</p>
          <div>Cout Amphitheatre :</div>
          <p class="text-h4 text--primary">{{amphitheatre.cout}}</p>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="deep-purple accent-4"> Learn More </v-btn>
        </v-card-actions>
      </v-card>

      <h3 class=" mt-10 mb-6">Historique Conférence</h3>
      <v-data-table
        :headers="headers"
        :items="amphitheatres"
        sort-by="titre"
        class="elevation-1"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Liste des Conférences</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
           
         
          </v-toolbar>
        </template>
      
        <template v-slot:no-data>
          <v-btn color="primary" @click="initialize"> Charger </v-btn>
        </template>
      </v-data-table>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
   amphitheatre: {},
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
     
    ],
    amphitheatres: [],
    errors: [],
  }),

  computed: {
    
  },

  

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      let url = "amphitheatres/"+this.$route.params.id+"/";
      axios
        .get(url)
        .then((response) => {
          console.log(response);
          this.amphitheatre = response.data;
        })
        .catch((e) => {
          this.errors.push(e);
          console.log(e);
        });
    },
   

    showMessage(msg) {
      this.$toast.success(msg);
    },
  },
};
</script>

<style src="./Basic.scss" lang="scss"></style>
