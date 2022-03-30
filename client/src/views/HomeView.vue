<template>
  <div>
    <h3 class="uk-margin-top">Home</h3>
    <button @click="onClick">ev1</button>
    <post-edit></post-edit>
    <hr class="uk-margin-right" />
    <div>
      <post-panel
        v-for="post in posts"
        :key="post._id"
        :post="post"
      ></post-panel>
    </div>
  </div>
</template>

<script>
import { io } from "socket.io-client";
import { onMounted, computed } from "vue";
import { useStore } from "vuex";

import PostEdit from "@/components/PostEdit.vue";
import PostPanel from "@/components/PostPanel.vue";

export default {
  components: {
    PostEdit,
    PostPanel,
  },
  setup() {
    const store = useStore();

    onMounted(() => {
      store.dispatch("loadPosts");
    });

    const socket = io();
    const onClick = () => {
      socket.emit("ev1");
    };
    socket.on("resp1", (arg) => {
      console.log("resp1");
      console.log(arg);
    });
    socket.on("connected", (arg) => {
      console.log("connected");
      console.log(arg);
    });
    return {
      posts: computed(() => store.state.posts),
      onClick,
    };
  },
};
</script>
