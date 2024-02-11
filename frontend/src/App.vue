<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <v-app>
    <v-main class="elevation-2">
      <v-container>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>

</template>

<style scoped lang="css">
.v-main {
  background-color: var(--color-background-soft)
  /* padding: 0;
  margin: 0; */
}
</style>
