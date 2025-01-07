<template>
  <div>
    <v-card>
      <v-form v-model="valid">
        <v-container>
          <v-row class="text-h5 ml-2 font-weight-light mt-2 pd-2">
            Nová faktura
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                v-model="new_invoice.date"
                label="Datum YYYY-MM-DD"
                :rules="[required, is_date]"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-combobox
                v-model="new_invoice.paydate"
                label="Datum splatnosti za"
                :items="['7', '14', '30']"
                :rules="[required, is_number]"
              >
              </v-combobox>
            </v-col>
            <v-col>
              <v-text-field
                v-model="new_invoice.currency"
                label="Měna"
                :disabled="true"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
        <v-container class="align-center">
          <v-row
            v-for="(item, index) in items"
            :key="index"
            :item="item"
            align="center"
          >
            <v-col cols="7">
              <v-text-field
                v-model="item.description"
                label="Popis"
                density="compact"
                :rules="[required]"
              ></v-text-field>
            </v-col>
            <v-col cols="1">
              <v-text-field
                v-model="item.quantity"
                label="Množství"
                density="compact"
                :rules="[required, is_number]"
              ></v-text-field>
            </v-col>
            <v-col cols="2">
              <v-text-field
                v-model="item.price"
                label="Cena"
                density="compact"
                :rules="[required, is_number]"
              ></v-text-field>
            </v-col>
            <v-col cols="1">
              <v-text-field
                v-model="item.tax"
                label="DPH %"
                density="compact"
                :rules="[is_number]"
              ></v-text-field>
            </v-col>
            <v-col cols="1">
              <v-btn
                class="mb-5 my-btn"
                @click="items.splice(index, 1)"
                :disabled="items.length <= 1"
                icon="mdi-close"
                density="comfortable"
                size="small"
              >
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
        <v-container>
          <v-row justify="space-between" align="center">
            <v-col cols="auto">
              <v-btn class="my-btn" @click="addItem">Přidat položku</v-btn>
            </v-col>
            <v-col cols="auto">
              <div class="text-disabled">
                Celkem {{ amountSum }} CZK, splatnost {{ dueDate }}
              </div>
            </v-col>
            <v-col cols="auto">
              <v-btn
                class="my-btn mr-2"
                :disabled="!valid"
                @click="newInvoice(false)"
              >
                Ukázat náhled
              </v-btn>
              <v-btn class="my-btn" :disabled="!valid" @click="newInvoice(true)"
                >Vytvořit fakturu</v-btn
              >
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, reactive } from "vue";
import useFetching from "@/js/useFetching";
import { ru } from "vuetify/locale";

const { Axios } = useFetching();

const props = defineProps(["client_id", "provider_id"]);
const emit = defineEmits(["updated", "close"]);

const valid = ref(false);
const required = (v: string) => !!v || "Povinné pole";
const is_number = (v: string) => !isNaN(parseFloat(v)) || "Musí být číslo";
const is_date = (v: string) => v.match(/^\d{4}-\d{2}-\d{2}$/) || "Musí být ve formátu YYYY-MM-DD";

interface Item {
  description: string;
  quantity: number;
  price: number;
  tax: number;
}

interface Invoice {
  item_list: Item[];
  date: string;
  paydate: string;
  currency: string;
  save: boolean;
}

const items = reactive<Item[]>([
  { description: "", quantity: 1, price: 0, tax: 0 },
]);
const amountSum = computed(() =>
  items.reduce((acc, item) => acc + item.quantity * item.price, 0)
);

function addItem() {
  //push an empty item to the items array:
  items.push({ description: "", quantity: 1, price: 0, tax: 0 });
}

const new_invoice = ref<Invoice>({
  item_list: [],
  date: new Date().toISOString().slice(0, 10),
  paydate: "7",
  currency: "CZK",
  save: false,
});

const dueDate = computed(() => {
  try {
    return new Date(
      new Date(new_invoice.value.date).setDate(
        new Date(new_invoice.value.date).getDate() +
          parseInt(new_invoice.value.paydate)
      )
    )
      .toISOString()
      .slice(0, 10);
  } catch (_error) {
    return "- nevalidní datum";
  }
});

async function newInvoice(save: boolean) {
  const invoice = {
    provider_id: props.provider_id,
    client_id: props.client_id,
    item_list: items,
    date: new_invoice.value.date,
    paydate: dueDate.value,
    currency: new_invoice.value.currency,
    save: save,
  };
  try {
    console.log(invoice);
    const response = await Axios.post("invoice/new", invoice);
    console.log(response.data);
    window.open(`/static/${response.data.path}`, "_blank");
    emit("updated");
    if (save) {
      emit("close");
    }
  } catch (error) {
    console.error(error);
  }
}
</script>

<style scoped>
.my-btn {
  background-color: var(--color-background-mute);
}
</style>
