<template>
  <div class="uk-modal-dialog uk-modal-body">
    <button class="uk-modal-close-default" type="button" uk-close></button>
    <simple-post-panel
      v-if="Boolean(post)"
      :post="post"
      :disableLink="true"
    ></simple-post-panel>
    <div class="uk-flex uk-flex-top">
      <avatar-pic :user="userLoggedIn" :disableLink="true"></avatar-pic>
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
import SimplePostPanel from "@/components/SimplePostPanel.vue";

export default {
  components: {
    AvatarPic,
    SimplePostPanel,
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
          context.emit("replySuccess");
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