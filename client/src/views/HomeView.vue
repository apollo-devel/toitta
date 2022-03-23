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
        @clickReply="onReplyClick"
      ></post-panel>
    </div>
    <div id="reply-modal" uk-modal>
      <reply-modal @closeModal="closeModal"></reply-modal>
    </div>
    <button uk-toggle="target: #reply-modal">open</button>
  </div>
</template>

<script>
import UIkit from "uikit";
import { onMounted, computed } from "vue";
import { useStore } from "vuex";

import PostEdit from "@/components/PostEdit.vue";
import PostPanel from "@/components/PostPanel.vue";
import ReplyModal from "@/components/ReplyModal.vue";

export default {
  components: {
    PostEdit,
    PostPanel,
    ReplyModal,
  },
  setup() {
    const store = useStore();

    onMounted(() => {
      store.dispatch("loadPosts");
    });

    const onReplyClick = (post) => {
      store.dispatch("openReplyModal", { post }).then(() => {
        const element = document.getElementById("reply-modal");
        UIkit.modal(element).show();
      });
    };

    const closeModal = () => {
      const element = document.getElementById("reply-modal");
      UIkit.modal(element).hide();
    };

    return {
      posts: computed(() => store.state.posts),
      onReplyClick,
      closeModal,
    };
  },
};
</script>
