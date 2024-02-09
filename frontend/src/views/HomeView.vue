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
         <v-select class="selector" label="Poskytovatel" :items="entities" item-title="abbreviation" item-value="id"></v-select>
      </v-col>
      <v-col cols="auto">
         <v-select class="selector" label="Odběratel" :items="entities" item-title="abbreviation" item-value="id"></v-select>
      </v-col>
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
import { onMounted, ref } from "vue";
import EntityForm from "@/components/EntityForm.vue";
import { fa } from "vuetify/locale";
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
