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
    <v-row >
      <v-col cols="auto">
         <v-select class="selector" label="Poskytovatel" v-model="provider_id" :items="entities" item-title="abbreviation" item-value="id"></v-select>
      </v-col>
      <v-col cols="auto">
         <v-select class="selector" label="Odběratel" v-model="client_id" :items="entities" item-title="abbreviation" item-value="id"></v-select>
      </v-col>
    </v-row>
    <v-row v-for="invoice in existing_invoices" :key="invoice.name">
      <v-col cols="12" sm="1" justify="left"><v-icon icon="mdi-file-pdf-box"></v-icon></v-col>
      <v-col cols="12" sm="5" justify="left"> {{ invoice.name }} </v-col>
      <v-col cols="12" sm="4" justify="left"> {{ new Date(invoice.modify_time*1000).toLocaleString('cs') }} </v-col>
      <v-col cols="12" sm="2" justify="right">
          <v-btn :href="`static/${invoice.path}`" target="_blank">otevřít</v-btn>
      </v-col>
      <v-divider></v-divider>
    </v-row>
  </v-container>

  <v-container v-if="subjekty">
    Subjekty:
    <v-data-table
      :headers="headers"
      :items="entities"
      items-per-page-text="Subjektů na stránku"
    >
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
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import EntityForm from "@/components/EntityForm.vue";
import useFetching from "@/js/useFetching";

const {Axios} = useFetching();

const showForm = ref(false);
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
    const response = await Axios.get(`invoice/list/${provider_id.value}/${client_id.value}`)
    console.log(response.data);
    existing_invoices.value = response.data;
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
