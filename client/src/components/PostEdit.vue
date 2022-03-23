<template>
  <form @submit="onSubmit">
    <div class="uk-flex uk-flex-top">
      <avatar-pic :user="user"></avatar-pic>
      <textarea
        v-model="content"
        placeholder="いまどうしてる？"
        class="uk-textarea uk-margin-left textarea"
      ></textarea>
    </div>
    <div class="uk-flex uk-flex-right">
      <input
        class="uk-button uk-button-primary uk-margin-right"
        type="submit"
        value="ツイートする"
        :disabled="isInvalid"
      />
    </div>
  </form>
</template>

<script>
import UIkit from "uikit";
import { computed, ref } from "vue";
import { useStore } from "vuex";

import AvatarPic from "@/components/AvatarPic.vue";

export default {
  components: {
    AvatarPic,
  },
  setup() {
    const store = useStore();

    const content = ref("");

    const isInvalid = computed(() => {
      const value = content.value;
      if (value.trim().length === 0) {
        return true;
      }

      if (value.length > 140) {
        return true;
      }

      return false;
    });

    const onSubmit = (e) => {
      e.preventDefault();

      store
        .dispatch("createPost", { content: content.value })
        .then(() => {
          content.value = "";
        })
        .catch((error) => {
          UIkit.notification(error.response.data.error.message, {
            status: "danger",
          });
        });
    };

    const user = computed(() => store.state.userLoggedIn);
    return {
      content,
      onSubmit,
      isInvalid,
      user,
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