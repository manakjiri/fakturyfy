<template>
  <v-container style="width=1500px">
    <v-row justify="space-between">
      <v-col cols="auto">
        <v-btn>Faktury</v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn>Subjekty</v-btn>
      </v-col>
    </v-row>
  </v-container>

  <v-container>
    <v-data-table :headers="headers" :items="entities" items-per-page-text="Subjektů na stránku"> 
      <template v-slot:item.edit="{ item }">
      <v-icon icon="mdi-magnify-expand"></v-icon>
    </template>
    </v-data-table>
  </v-container>

  <v-form>
    <v-container>
      <v-row>
        <v-col>
          <!-- v-model="firstname"
            :rules="nameRules" -->
          <v-text-field
            v-model="form_values.name"
            label="Jméno"
            required
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            v-model="form_values.abbreviation"
            label="Zkratka"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="form_values.ic_number"
            label="IČO"
            required
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            v-model="form_values.tax_number"
            label="DIČ"
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            v-model="form_values.tax_note"
            label="Daňová poznámka"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="form_values.bank_account"
            label="Bankovní účet"
            required
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            v-model="form_values.bank_code"
            label="Kod banky"
            required
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            v-model="form_values.bank_name"
            label="Jméno banky"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="form_values.address"
            label="Adresa"
            required
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            v-model="form_values.zip_code"
            label="PSČ"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="form_values.city"
            label="Město"
            required
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            v-model="form_values.country"
            label="Stát"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="form_values.email"
            label="E-mail"
          ></v-text-field>
        </v-col>
        <v-col>
          <v-text-field
            v-model="form_values.phone"
            label="Telefon"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
    <v-btn @click="newEntity">Uložit</v-btn>
  </v-form>
  
  {{ form_values }}


</template>

<script setup lang="ts">

import axios from 'axios'
import { onMounted, ref } from 'vue';

const form_values = ref({
  name: '',
  abbreviation: '',
  ic_number: '',
  tax_number: '',
  tax_note: '',
  bank_account: '',
  bank_code: '',
  bank_name: '',
  address: '',
  zip_code: '',
  city: '',
  country: '',
  email: '',
  phone: '',
  logo: null,
});


const headers = [
  { title: "Jméno", value: "name" , sortable: true},
  { title: "Zkratka", value: "abbreviation", sortable: true},
  { title: "IČO", value: "ic_number" },
  { title: "DIČ", value: "tax_number" },
  { title: "Info/Edit", value: "edit"}
];

const Axios = axios.create({
    baseURL: `http://127.0.0.1:8000/api/`,
    timeout: 5000,
});

async function getEntities() {
  console.log('getEntities');
  try {
    const response = await Axios.get('entity');
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

async function newEntity() {
  console.log('newEntity');
  try {
    const response = await Axios.post('entity/', form_values.value);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

const entities = ref();

onMounted(async () => {
  entities.value = await getEntities();
});

</script>
