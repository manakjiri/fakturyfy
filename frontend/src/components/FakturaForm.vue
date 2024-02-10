<template>
  <div>
    <v-card>
      <v-form>
        <v-container>
            <v-row class="text-h5 ml-2 font-weight-light mt-2 pd-2">
                Nová faktura
            </v-row>
          <v-row>
            <v-col>
              <v-text-field
                v-model="new_invoice.date"
                label="Datum"
                required
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="new_invoice.paydate"
                label="Datum splatnosti"
                required
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="new_invoice.currency"
                label="Měna"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row v-for="(item, index) in items" :key="index" :item="item">
              <v-col>
                <v-text-field
                  v-model="item.description"
                  label="Popis"
                  required
                ></v-text-field>
              </v-col>
              <v-col>
                <v-text-field
                  v-model="item.quantity"
                  label="Množství"
                  required
                ></v-text-field>
              </v-col>
              <v-col>
                <v-text-field
                  v-model="item.price"
                  label="Cena"
                  required
                ></v-text-field>
              </v-col>
              <v-col>
                <v-text-field
                  v-model="item.tax"
                  label="DPH"
                  required
                ></v-text-field>
              </v-col>
          </v-row>
          <v-row justify="space-between">
                <v-col cols="auto">
                    <v-btn style="background-color: rgb(101, 101, 101);" @click="addItem">Přidat položku</v-btn>
                </v-col>
                <v-col cols="auto">
                    <v-btn style="background-color: rgb(101, 101, 101);" @click="newInvoice">Vytvořit fakturu</v-btn>
                </v-col>
          </v-row>
        </v-container>
        
      </v-form>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive } from "vue";
import useFetching from "@/js/useFetching";

const { Axios } = useFetching();

const props = defineProps(['client_id', 'provider_id']);

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

//const items = reactive([{ description: "", quantity: "", price: "", tax: "" }]);
const items = reactive<Item[]>([
  { description: "", quantity: 0, price: 0, tax: 0 },
]);

function addItem() {
  //push an empty item to the items array:
  items.push({ description: "", quantity: 0, price: 0, tax: 0 });
}

const new_invoice = ref<Invoice>({
  item_list: [],
  date: new Date().toISOString().slice(0, 10),
  paydate: new Date(new Date().setMonth(new Date().getMonth() + 1)).toISOString().slice(0, 10),
  currency: "CZK",
  save: false,
});

async function newInvoice() {
  const invoice = {
    provider_id: props.provider_id,
    client_id: props.client_id,
    item_list: items,
    date: new_invoice.value.date,
    paydate: new_invoice.value.paydate,
    currency: new_invoice.value.currency,
    save: true,
  };
  try {
    console.log(invoice);
    const response = await Axios.post("invoice/new", invoice);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}
</script>
