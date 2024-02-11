<template>
  <div>
    <v-card>
      <v-form>
        <v-container>
          <v-row class="text-h5 ml-2 font-weight-light mt-2 pd-2">
            Subjekt
          </v-row>
          <v-row>
            <v-col>
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
                label="Poznámka"
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
          <v-row justify="space-between">
            <v-col cols="auto"> </v-col>
            <v-col cols="auto">
              <v-btn class="my-button" @click="newEntity">Uložit</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import useFetching from "@/js/useFetching";

const { Axios } = useFetching();

const showForm = ref(false);

const props = defineProps(["entity_id"]);

interface Entity {
  name: string;
  abbreviation: string;
  ic_number: string;
  tax_number: string;
  tax_note: string;
  bank_account: string;
  bank_code: string;
  bank_name: string;
  address: string;
  zip_code: string;
  city: string;
  country: string;
  email: string;
  phone: string;
  logo: string | null;
}

const form_values = ref<Entity>(createEmptyEntity());

function createEmptyEntity(){
  return {
    name: "",
    abbreviation: "",
    ic_number: "",
    tax_number: "",
    tax_note: "",
    bank_account: "",
    bank_code: "",
    bank_name: "",
    address: "",
    zip_code: "",
    city: "",
    country: "",
    email: "",
    phone: "",
    logo: null,
  }
}

//create form values as computed, empty if entity_id is null, else fetch the entity:
onMounted(() => {
  if (props.entity_id) {
    fetchEntity();
  } else {
    form_values.value = createEmptyEntity();
  }
});

async function newEntity() {
  console.log("newEntity");
  try {
    const req = form_values.value;
    console.log(req);
    const response = await Axios.post("entity/", req);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

async function fetchEntity() {
  console.log("fetchEntity");
  try {
    const response = await Axios.get(`entity/${props.entity_id}`);
    console.log(response.data);
    form_values.value = response.data;
  } catch (error) {
    console.error(error);
  }
}

const entities = ref();
</script>

<style scoped>
.my-button {
  background-color: rgb(101, 101, 101);
}
</style>
