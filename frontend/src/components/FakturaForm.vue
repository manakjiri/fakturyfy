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
              ></v-text-field>
            </v-col>
            <v-col>
              <v-combobox
                v-model="new_invoice.paydate"
                label="Datum splatnosti za"
                :items="['7', '14', '30']"
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
          <v-row
            style="height: 65px"
            v-for="(item, index) in items"
            :key="index"
            :item="item"
          >
            <v-col>
              <v-text-field
                v-model="item.description"
                label="Popis"
                density="compact"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="item.quantity"
                label="Množství"
                density="compact"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="item.price"
                label="Cena"
                density="compact"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="item.tax"
                label="DPH"
                density="compact"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row justify="space-between">
            <v-col cols="auto">
              <v-btn class="my-btn" @click="addItem">Přidat položku</v-btn>
            </v-col>
            <v-col cols="auto">
              <v-btn class="my-btn mr-2" @click="newInvoice(false)">
                Ukázat náhled
              </v-btn>
              <v-btn class="my-btn" @click="newInvoice(true)"
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
import { onMounted, ref, reactive } from "vue";
import useFetching from "@/js/useFetching";

const { Axios } = useFetching();

const props = defineProps(["client_id", "provider_id"]);
const emit = defineEmits(["updated", "close"]);


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
  { description: "", quantity: 0, price: 0, tax: 0 },
]);

function addItem() {
  //push an empty item to the items array:
  items.push({ description: "", quantity: 0, price: 0, tax: 0 });
}

const new_invoice = ref<Invoice>({
  item_list: [],
  date: new Date().toISOString().slice(0, 10),
  paydate: '7',
  currency: "CZK",
  save: false,
});

async function newInvoice(save: boolean) {
  const invoice = {
    provider_id: props.provider_id,
    client_id: props.client_id,
    item_list: items,
    date: new_invoice.value.date,
    paydate: new Date(
      new Date().setDate(new Date(new_invoice.value.date).getDate() + parseInt(new_invoice.value.paydate))
    )
      .toISOString()
      .slice(0, 10),
    currency: new_invoice.value.currency,
    save: save,
  };
  try {
    console.log(invoice);
    const response = await Axios.post("invoice/new", invoice);
    console.log(response.data);
    window.open(`/static/${response.data.path}`, '_blank');
    emit("updated");
    if(save){
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
