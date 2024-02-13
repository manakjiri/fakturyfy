<template>
  <div>
    <v-card>
      <v-form v-model="valid">
        <v-container>
          <v-row class="text-h5 ml-2 font-weight-light mt-2 pd-2">
            Subjekt
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                v-model="form_values.name"
                label="Název (*)"
                :rules="[required]"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                label="Zkratka (*)"
                v-model="form_values.abbreviation"
                :rules="[required]"
              >
                <template #append>
                  <v-tooltip bottom>
                    <template #activator="{ props }">
                      <v-icon v-bind="props"> mdi-information-outline </v-icon>
                    </template>
                    Zkratka bude použita pro výběr subjektů při tvorbě faktury.<br>
                    Na fakturách bude název subjektu.
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                v-model="form_values.ic_number"
                label="IČO (*)"
                :rules="[required, constraint_number]"
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
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="form_values.bank_code"
                label="Kod banky"
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
                label="Adresa (*)"
                :rules="[required]"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="form_values.zip_code"
                label="PSČ (*)"
                :rules="[required]"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                v-model="form_values.city"
                label="Město (*)"
                :rules="[required]"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="form_values.country"
                label="Stát (*)"
                :rules="[required]"
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
            <!-- <v-col>
              <v-file-input
                v-model="form_values.logo"
                label="Logo"
                accept="image/*"
              ></v-file-input>
            </v-col> -->
            <v-col cols="auto"></v-col>
            <v-col cols="auto">
              <v-btn
                v-if="entity_id"
                class="my-button mr-2"
                color="#965151"
                @click="deleteEntity"
                >Smazat</v-btn
              >
              <v-btn :disabled="!valid" class="my-button" @click="editEntity"
                >Uložit</v-btn
              >
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
const valid = ref(false);
const showTooltip = ref(false);

const props = defineProps(["entity_id"]);
const emit = defineEmits(["updated", "close"]);

const required = (v: string) => !!v || "Povinné pole";
const constraint_number = (v: string) => Number(v).toString() == v || "Musí být číslo";

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
  logo: any;
}

const form_values = ref<Entity>(createEmptyEntity());

function createEmptyEntity() {
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
  };
}

//create form values as computed, empty if entity_id is null, else fetch the entity:
onMounted(() => {
  if (props.entity_id) {
    fetchEntity();
  } else {
    form_values.value = createEmptyEntity();
  }
});

/* function onInfoIconClick() {
  showTooltip.value = !showTooltip.value;
} */

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

async function readFile(file: any) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = async () => {
      try {
        // Resolve the promise with the response value
        /* resolve({
          'image': reader.result,
          'name': file.name
        }); */
        console.log("reader.result");
        console.log(reader.result);
        resolve(reader.result);
      } catch (err) {
        reject(err);
      }
    };
    reader.onerror = (error) => {
      reject(error);
    };
    reader.readAsDataURL(file);
  });
}

async function updateEntity() {
  console.log("updateEntity");
  try {
    const req = form_values.value;
    console.log(req);
    const response = await Axios.put(`entity/${props.entity_id}/`, req);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

async function editEntity() {
  console.log("editEntity");
  if (props.entity_id) {
    await updateEntity();
  } else {
    await newEntity();
  }
  emit("updated");
  emit("close");
}

async function deleteEntity() {
  console.log("deleteEntity");
  const response = await Axios.delete(`entity/${props.entity_id}`);
  emit("updated");
  emit("close");
}
</script>

<style scoped>
.my-button {
  background-color: rgb(101, 101, 101);
}
</style>
