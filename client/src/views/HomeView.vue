<template>
  <div>
    <h3 class="uk-margin-top">Home</h3>
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

    return {
      posts: computed(() => store.state.posts),
    };
  },
};
</script>
