<template>
  <div class="uk-height-1-1">
    <component v-bind:is="layout()"></component>
  </div>
</template>

<script>
import { io } from "socket.io-client";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import DefaultLayout from "@/components/layouts/DefaultLayout.vue";
import SimpleLayout from "@/components/layouts/SimpleLayout.vue";

export default {
  components: {
    DefaultLayout,
    SimpleLayout,
  },
  setup() {
    const route = useRoute();
    const layout = () => {
      return route.meta.layout ? route.meta.layout : "default-layout";
    };

    const store = useStore();
    const socket = io();
    socket.onAny((event, ...args) => {
      store.dispatch("handleSocketEvent", { event, args });
    });
    store.dispatch("setSocket", { socket });
    return {
      layout,
    };
  },
};
</script>
