<template>
  <div class="uk-width-1-1 uk-position-relative">
    <h3 class="uk-margin-small-top uk-margin-small-bottom">
      {{ username }}
    </h3>
    <div class="cover uk-margin-right"></div>
    <img
      :src="imageUrl(user)"
      class="uk-position-absolute uk-border-circle uk-margin-small-left avatar"
    />
    <div class="uk-width-1-1 uk-position-absolute" v-if="user._id">
      <div
        class="uk-flex uk-flex-row uk-flex-top uk-margin-right uk-margin-small-top buttons"
      >
        <div class="uk-flex-1"></div>
        <button
          class="uk-button uk-button-default uk-button-small uk-text-bold"
        >
          プロフィールを編集
        </button>
      </div>
      <div class="uk-flex uk-flex-column uk-flex-left uk-margin-small-left">
        <div class="uk-text-large uk-text-bold">{{ user.display_name }}</div>
        <div>@{{ user.username }}</div>
        <div class="uk-margin-small-top">{{ user.description }}</div>
        <div class="uk-margin-small-top">
          <span class="uk-text-bold">100</span>
          <span class="uk-margin-right">フォロー中</span>
          <span class="uk-text-bold">50</span>
          <span>フォロワー</span>
        </div>
      </div>
      <div class="uk-margin-top uk-margin-right">
        <ul class="uk-child-width-expand" ref="tabs" uk-tab uk-switcher>
          <li><a>ツイート</a></li>
          <li><a>ツイートと返信</a></li>
          <li><a>いいね</a></li>
        </ul>
        <ul class="uk-switcher">
          <div>ツイートです</div>
          <div>ツイートと返信です</div>
          <div>いいねです</div>
        </ul>
      </div>
    </div>
    <div class="uk-position-absolute error-message" v-else>
      <h3>ユーザーが存在しません</h3>
    </div>
  </div>
</template>

<script>
import { computed, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import { imageUrl } from "@/functions/avatar.js";

export default {
  setup() {
    const route = useRoute();
    const store = useStore();

    const username = route.params.username
      ? route.params.username
      : store.state.userLoggedIn.username;

    onBeforeMount(async () => {
      await store.dispatch("loadProfileUser", username).catch(() => {
        // noop
      });
    });

    const user = computed(() => store.state.profile.user);
    return {
      username,
      user,
      imageUrl,
    };
  },
};
</script>

<style scoped>
.cover {
  background-color: lightslategray;
  height: 180px;
}

.avatar {
  width: 132px;
  height: 132px;
  bottom: -66px;
  border: 4px solid #fff;
}

.buttons {
  height: 60px;
}

.error-message {
  margin-top: 30px;
  margin-left: 132px;
}
</style>