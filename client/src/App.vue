<template>
  <div>
    <component v-bind:is="layout()"></component>
  </div>
</template>

<script>
import { useRoute } from 'vue-router';
import DefaultLayout from '@/components/layouts/DefaultLayout.vue';
import SimpleLayout from '@/components/layouts/SimpleLayout.vue';

export default {
  components: {
    DefaultLayout,
    SimpleLayout
  },
  setup() {
    const route = useRoute();
    const layout = () => {
      return route.meta.layout ? route.meta.layout : 'default-layout';
    };
    return {
      layout
    }
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
