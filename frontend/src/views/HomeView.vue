<template>
  <v-container class="zapati" style="width=1500px">
    <v-row justify="space-between">
      <v-col cols="auto">
        <v-btn @click="fakturyView">Faktury</v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn @click="subjektyView">Subjekty</v-btn>
      </v-col>
    </v-row>
  </v-container>

  <v-container v-if="faktury">
    <v-row>
      <v-col cols="3">
        <v-select class="selector" label="Poskytovatel" :append-icon="'mdi-close'" @click:append="clearSelectionProvider"
          v-model="provider_id" :items="entities" item-title="abbreviation" item-value="id"></v-select>
      </v-col>
      <v-col cols="3">
        <v-select class="selector" label="Odběratel" :append-icon="'mdi-close'" @click:append="clearSelectionClient"
          v-model="client_id" :items="entities" item-title="abbreviation" item-value="id"></v-select>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="3">
        <v-btn @click="showFakturaForm = true">Nová faktura</v-btn>
      </v-col>
    </v-row>

    <v-container v-if="existing_invoices">
      <v-row v-for="invoice in existing_invoices" :key="invoice.name" justify="space-between">
        <v-col cols="9" align-self="center">
          <v-row no-gutters justify="start">
            <v-col cols="1"><v-icon icon="mdi-file-pdf-box"></v-icon></v-col>
            <v-col><v-sheet>{{ invoice.name }}</v-sheet></v-col>
            <v-col><v-sheet>{{ invoice.provider }} → {{ invoice.client }}</v-sheet></v-col>
            <v-col><v-sheet>{{ new Date(invoice.modify_time * 1000).toLocaleString('cs') }}</v-sheet></v-col>
          </v-row>
        </v-col>
        <v-col><v-spacer></v-spacer></v-col>
        <v-col cols="2" align-self="center">
          <v-btn :href="`static/${invoice.path}`" target="_blank">otevřít</v-btn>
        </v-col>
        <v-divider></v-divider>
      </v-row>
    </v-container>
  </v-container>

  <v-container v-if="subjekty">
    Subjekty:
    <v-data-table :headers="headers" :items="entities" items-per-page-text="Subjektů na stránku">
      <template v-slot:item.edit="{ item }">
        <v-icon icon="mdi-magnify-expand"></v-icon>
      </template>
    </v-data-table>
    <v-row justify="space-between">
      <v-col cols="auto"> </v-col>
      <v-col cols="auto">
        <v-btn @click="showForm = true">Nový subjekt</v-btn>
      </v-col>
    </v-row>
  </v-container>

  <v-container>
    <v-dialog v-model="showForm" scrim="true" class="form">
      <EntityForm></EntityForm>
    </v-dialog>
  </v-container>

  <v-container>
    <v-dialog v-model="showFakturaForm" scrim="true" class="form">
      <FakturaForm></FakturaForm>
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
  provider: string;
  client: string;
  modify_time: number;
}

const client_id = ref<number | null>(null);
const provider_id = ref<number | null>(null);
const existing_invoices = ref<Array<InvoiceDescription>>([
  /*   { path: "path", name: "name", modify_time: 0 },
    { path: "path", name: "name", modify_time: 1000000000 },
    { path: "path", name: "name", modify_time: 10000000000 }, */
]);

function clearSelectionClient() {
  client_id.value = null;
}

function clearSelectionProvider() {
  provider_id.value = null;
}

watch([client_id, provider_id], async () => {
  if (client_id.value || provider_id.value) {
    console.log("updateExistingInvoices");
    const req = { client_id: client_id.value, provider_id: provider_id.value };
    const response = await Axios.get(`invoice/list`, { params: req })
    console.log(response.data);
    existing_invoices.value = response.data;
  }
  else {
    existing_invoices.value = [];
  }
});

const headers = [
  { title: "Jméno", value: "name", sortable: true },
  { title: "Zkratka", value: "abbreviation", sortable: true },
  { title: "IČO", value: "ic_number" },
  { title: "DIČ", value: "tax_number" },
  { title: "Info/Edit", value: "edit" },
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

onMounted(async () => {
  entities.value = await getEntities();
});
</script>

<style>
.form {
  width: 1200px;
}

.zapati {
  background-color: antiquewhite;
}

.selector {
  width: 200px;
}
</style>
