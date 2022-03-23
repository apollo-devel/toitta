<template>
  <div class="uk-modal-dialog uk-modal-body">
    <post-panel v-if="Boolean(post)" :post="post"></post-panel>
    <div class="uk-flex uk-flex-top">
      <avatar-pic :user="userLoggedIn"></avatar-pic>
      <textarea
        v-model="content"
        placeholder="返信をツイート"
        class="uk-textarea uk-margin-left textarea"
      ></textarea>
    </div>
    <p class="uk-text-right">
      <button
        class="uk-button uk-button-primary"
        type="button"
        @click="onReplyClick"
      >
        返信
      </button>
    </p>
  </div>
</template>

<script>
import UIkit from "uikit";
import { computed, ref } from "vue";
import { useStore } from "vuex";

import AvatarPic from "@/components/AvatarPic.vue";
import PostPanel from "@/components/PostPanel.vue";

export default {
  components: {
    AvatarPic,
    PostPanel,
  },
  setup(_, context) {
    const store = useStore();

    const post = computed(() => store.state.replyTo);

    const userLoggedIn = computed(() => store.state.userLoggedIn);

    const onReplyClick = () => {
      store
        .dispatch("createPost", {
          content: content.value,
          reply_to: post.value._id,
        })
        .then(() => {
          content.value = "";
          context.emit("closeModal");
        })
        .catch((error) => {
          UIkit.notification(error.response.data.error.message, {
            status: "danger",
          });
        });
    };
    const content = ref("");
    return {
      post,
      userLoggedIn,
      content,
      onReplyClick,
    };
  },
};
</script>

<style scoped>
.textarea {
  resize: none;
  border: 0;
  height: 100px;
  margin-top: 5px;
}
</style>