<template>
  <div>
    <h3 class="uk-margin-top">ツイート</h3>
    <post-panel
      v-if="Boolean(post.reply_to)"
      :post="post.reply_to"
    ></post-panel>
    <post-panel :post="post"></post-panel>
    <post-panel
      v-for="reply in post.replies"
      :post="reply"
      :key="reply._id"
    ></post-panel>
  </div>
</template>

<script>
import { computed, watch } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import PostPanel from "@/components/PostPanel.vue";

export default {
  components: {
    PostPanel,
  },
  setup() {
    const route = useRoute();
    const store = useStore();

    watch(
      () => route.params.postId,
      (postId) => {
        store.dispatch("loadPost", { postId });
      },
      {
        immediate: true,
      }
    );

    const post = computed(() => store.state.post);

    return {
      post,
    };
  },
};
</script>
