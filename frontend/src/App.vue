<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <v-app class="elevation-2">
    <v-main >
      <v-container>
        <router-view></router-view>
      </v-container>
    </v-main>
    <v-footer class="footer d-flex flex-column">
      <v-row align="end" justify="center">
        <v-col cols="auto">
          Fakturyfy <a href="https://github.com/manakjiri/fakturyfy" target="_blank"><v-icon icon="mdi-github"></v-icon> GitHub </a>
          <br>
          &copy; 2024 <a href="https://github.com/xdxdhh" target="_blank">diana_v</a> & <a href="https://github.com/manakjiri" target="_blank">manakjiri</a>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>

</template>

<style scoped lang="css">
.v-main {
  background-color: var(--color-background-soft)
  /* padding: 0;
  margin: 0; */
}

.footer {
  background-color: var(--color-background-soft);
  text-align: center;
  padding: 50px;
}
</style>
