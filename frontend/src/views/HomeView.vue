<template>
  <v-container class="zapati elevation-3">
    <v-row justify="space-between">
      <v-col cols="auto">
        <v-btn class="my-button" @click="fakturyView">Faktury</v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn class="my-button" @click="subjektyView">Subjekty</v-btn>
      </v-col>
    </v-row>
  </v-container>

  <v-container v-if="faktury">
    <v-row>
      <v-col cols="auto">
        <v-select
          class="selector"
          label="Poskytovatel"
          v-model="provider_id"
          :items="entities"
          item-title="abbreviation"
          item-value="id"
        ></v-select>
      </v-col>
      <v-col cols="auto">
        <v-select
          class="selector"
          label="Odběratel"
          v-model="client_id"
          :items="entities"
          item-title="abbreviation"
          item-value="id"
        ></v-select>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="auto">
        <v-btn class="my-button" @click="showFakturaForm = true"
          >Nová faktura</v-btn
        >
      </v-col>
    </v-row>

    <v-row v-for="invoice in existing_invoices" :key="invoice.name">
      <v-col cols="12" sm="1" justify="left"
        ><v-icon icon="mdi-file-pdf-box"></v-icon
      ></v-col>
      <v-col cols="12" sm="5" justify="left"> {{ invoice.name }} </v-col>
      <v-col cols="12" sm="4" justify="left">
        {{ new Date(invoice.modify_time * 1000).toLocaleString("cs") }}
      </v-col>
      <v-col cols="12" sm="2" justify="right">
        <v-btn :href="`static/${invoice.path}`" target="_blank">otevřít</v-btn>
      </v-col>
      <v-divider></v-divider>
    </v-row>
  </v-container>

  <v-container v-if="subjekty">
    <v-row class="text-h5 mt-2 mb-2 font-weight-light"> Subjekty: </v-row>
    <v-row>
      <v-data-table
        class="my-data-table elevation-2"
        :headers="headers"
        :items="entities"
        items-per-page-text="Subjektů na stránku"
      >
        <template v-slot:item.edit="{ item }">
          <v-icon @click="editEntity(item)" icon="mdi-magnify-expand"></v-icon>
        </template>
      </v-data-table>
    </v-row>

    <v-row justify="space-between">
      <v-col cols="auto"> </v-col>
      <v-col cols="auto">
        <v-btn class="my-button" @click="createNewEntity">Nový subjekt</v-btn>
      </v-col>
    </v-row>
  </v-container>

  <v-container>
    <v-dialog v-model="showForm" scrim="true" class="form">
      <EntityForm :entity_id="chosenEntityId"></EntityForm>
    </v-dialog>
  </v-container>

  <v-container>
    <v-dialog v-model="showFakturaForm" scrim="true" class="form">
      <FakturaForm
        :client_id="client_id"
        :provider_id="provider_id"
      ></FakturaForm>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import EntityForm from "@/components/EntityForm.vue";
import FakturaForm from "@/components/FakturaForm.vue";
import useFetching from "@/js/useFetching";

const { Axios } = useFetching();

const showForm = ref(false);
const showFakturaForm = ref(false);
const faktury = ref(true);
const subjekty = ref(false);

function fakturyView() {
  faktury.value = true;
  subjekty.value = false;
}

function subjektyView() {
  faktury.value = false;
  subjekty.value = true;
}

interface InvoiceDescription {
  path: string;
  name: string;
  modify_time: number;
}

const client_id = ref<number | null>(null);
const provider_id = ref<number | null>(null);
const existing_invoices = ref<Array<InvoiceDescription>>([]);

watch([client_id, provider_id], async () => {
  if (client_id.value && provider_id.value) {
    console.log("updateExistingInvoices");
    const response = await Axios.get(
      `invoice/list/${provider_id.value}/${client_id.value}`
    );
    console.log(response.data);
    existing_invoices.value = response.data;
  }
});

const headers = [
  { title: "JMÉNO", value: "name", sortable: true },
  { title: "ZKRATKA", value: "abbreviation", sortable: true },
  { title: "IČO", value: "ic_number", sortable: true },
  { title: "DIČ", value: "tax_number" },
  { title: "INFO/ÚPRAVA", value: "edit" },
];

async function getEntities() {
  console.log("getEntities");
  try {
    const response = await Axios.get("entity");
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

const entities = ref();
const chosenEntityId = ref<number | null>(null);

function createNewEntity() {
  console.log("createNewEntity");
  chosenEntityId.value = null;
  showForm.value = true;
}

function editEntity(item: any) {
  console.log("editEntity");
  console.log(item);
  chosenEntityId.value = item.id;
  console.log(chosenEntityId.value);
  showForm.value = true;
}

onMounted(async () => {
  entities.value = await getEntities();
});
</script>

<style scoped>
.form {
  width: 1200px;
}

.zapati {
  background-color: rgba(255, 255, 255, 0.1);
}

.selector {
  width: 200px;
}

.my-button {
  background-color: rgb(101, 101, 101);
}

.my-data-table {
  background-color: rgb(67, 67, 67);
}
</style>
