<template>
  <form @submit="onSubmit">
    <div class="uk-flex uk-flex-top">
      <img :src="url" class="uk-border-circle avatar" />
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
import { computed, ref } from "vue";
import { useStore } from "vuex";

import { imageUrl } from "@/functions/avatar.js";

export default {
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

      store.dispatch("createPost", content.value).then((success) => {
        if (success) {
          content.value = "";
        }
      });
    };

    const url = imageUrl(store.state.userLoggedIn);
    return {
      content,
      onSubmit,
      isInvalid,
      url,
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

.avatar {
  width: 50px;
  height: 50px;
}
</style>