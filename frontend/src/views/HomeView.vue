<template>
  <v-slide-x-transition>
    <v-container v-show="faktury">
      <v-container>
        <v-row justify="end">
          <v-col cols="auto">
            <v-btn
              variant="text"
              append-icon="mdi-arrow-right"
              size="x-large"
              @click="subjektyView"
              >Subjekty</v-btn
            >
          </v-col>
        </v-row>
      </v-container>
      <v-sheet
        class="d-flex align-center justify-center flex-wrap text-center mx-auto px-4"
        height="250"
        max-width="800"
        width="100%"
        color="rgba(0, 0, 0, 0)"
      >
        <v-row justify="space-between" align="start">
          <v-col cols="3">
            <v-select
              class="selector"
              label="Dodavatel"
              :append-icon="'mdi-close'"
              @click:append="clearSelectionProvider"
              v-model="provider_id"
              :items="providers"
              item-title="abbreviation"
              item-value="id"
            ></v-select>
          </v-col>
          <v-col cols="3">
            <v-select
              class="selector"
              label="Odběratel"
              :append-icon="'mdi-close'"
              @click:append="clearSelectionClient"
              v-model="client_id"
              :items="clients"
              item-title="abbreviation"
              item-value="id"
            ></v-select>
          </v-col>
          <v-col cols="3">
            <v-btn
              class="my-button"
              size="x-large"
              style="height: 57px"
              @click="showFakturaForm = true"
              :disabled="providerClientNotSelected"
              >Nová faktura</v-btn
            >
          </v-col>
        </v-row>
      </v-sheet>

      <v-card class="my-card ml-6 mr-6" v-if="existing_invoices.length > 0">
        <v-container>
          <v-row
            v-for="invoice in existing_invoices"
            :key="invoice.name"
            justify="space-between"
          >
            <v-col cols="9" align-self="center">
              <v-row no-gutters justify="start">
                <v-col cols="1"
                  ><v-icon icon="mdi-file-pdf-box"></v-icon
                ></v-col>
                <v-col>{{ invoice.name }}</v-col>
                <v-col>{{ invoice.provider }} → {{ invoice.client }}</v-col>
                <v-col>{{
                  new Date(invoice.modify_time * 1000).toLocaleString("cs")
                }}</v-col>
              </v-row>
            </v-col>
            <v-col><v-spacer></v-spacer></v-col>
            <v-col cols="2" align-self="center">
              <v-btn
                class="my-button"
                :href="`static/${invoice.path}`"
                target="_blank"
                >otevřít</v-btn
              >
              <!-- <v-icon color="#965151" class="ml-2" icon="mdi-close-circle"></v-icon> -->
            </v-col>
            <v-divider></v-divider>
          </v-row>
        </v-container>
      </v-card>
    </v-container>
  </v-slide-x-transition>

  <v-slide-x-reverse-transition>
    <v-container v-show="subjekty">
      <v-container>
        <v-row justify="start">
          <v-col cols="auto">
            <v-btn
              variant="text"
              prepend-icon="mdi-arrow-left"
              size="x-large"
              @click="fakturyView"
              >Faktury</v-btn
            >
          </v-col>
        </v-row>
      </v-container>

      <v-row class="text-h5 mt-15 mb-5 ml-5 font-weight-light"
        >Uložené subjekty</v-row
      >
      <v-row>
        <v-data-table
          class="my-data-table elevation-2 ml-6 mr-6"
          :headers="headers"
          :items="clients"
          items-per-page-text="Subjektů na stránku"
        >
          <template v-slot:item.edit="{ item }">
            <v-icon
              @click="editEntity(item)"
              icon="mdi-magnify-expand"
            ></v-icon>
          </template>
        </v-data-table>
      </v-row>

      <v-row justify="space-between" class="mr-2">
        <v-col cols="auto"> </v-col>
        <v-col cols="auto">
          <v-btn class="my-button" @click="createNewEntity">Nový subjekt</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-slide-x-reverse-transition>

  <v-container>
    <v-dialog v-model="showForm" scrim="true" class="form">
      <EntityForm
        @close="showForm = false"
        @updated="getEntities"
        :entity_id="chosenEntityId"
      ></EntityForm>
    </v-dialog>
  </v-container>

  <v-container>
    <v-dialog v-model="showFakturaForm" scrim="true" class="form">
      <FakturaForm
        @updated="updateExistingInvoices"
        @close="showFakturaForm = false"
        :client_id="client_id"
        :provider_id="provider_id"
      ></FakturaForm>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, ref, watch, computed } from "vue";
import EntityForm from "@/components/EntityForm.vue";
import FakturaForm from "@/components/FakturaForm.vue";
import useFetching from "@/js/useFetching";

const { Axios } = useFetching();

const showForm = ref(false);
const showFakturaForm = ref(false);
const faktury = ref(true);
const subjekty = ref(false);

function fakturyView() {
  subjekty.value = false;
  setTimeout(() => {
    faktury.value = true;
  }, 250);
}

function subjektyView() {
  faktury.value = false;
  setTimeout(() => {
    subjekty.value = true;
  }, 250);
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

const providerClientNotSelected = computed(() => {
  return !(client_id.value !== null && provider_id.value !== null);
});

watch([client_id, provider_id], async () => {
  if (client_id.value || provider_id.value) {
    updateExistingInvoices();
  } else {
    existing_invoices.value = [];
  }
});

async function updateExistingInvoices() {
  console.log("updateExistingInvoices");
  const req = { client_id: client_id.value, provider_id: provider_id.value };
  const response = await Axios.get(`invoice/list`, { params: req });
  console.log(response.data);
  existing_invoices.value = response.data;
}

const headers = [
  { title: "NÁZEV", value: "name", sortable: true },
  { title: "ZKRATKA", value: "abbreviation", sortable: true },
  { title: "IČO", value: "ic_number", sortable: true },
  { title: "ÚČET", value: "bank_account" },
  { title: "DETAIL", value: "edit" },
];

async function getEntities() {
  try {
    const response = await Axios.get("entity");
    clients.value = response.data;
    providers.value = response.data.filter((item: any) => item.bank_account);
  } catch (error) {
    console.error(error);
  }
}

const providers = ref();
const clients = ref();
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
  getEntities();
});
</script>

<style scoped>
.form {
  width: 1200px;
}

.zapati {
  background-color: var(--color-background-soft);
}

.selector {
  width: 250px;
}

.my-button {
  background-color: var(--color-background-mute);
}

.my-data-table {
  background-color: var(--color-background-soft);
}

.my-card {
  background-color: var(--color-background-soft);
}
</style>
