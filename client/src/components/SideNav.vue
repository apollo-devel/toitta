<template>
  <ul class="uk-iconnav uk-iconnav-vertical uk-padding">
    <li>
      <router-link
        to="/"
        uk-icon="icon: home; ratio: 2"
        uk-tooltip="title: ホーム; pos: right"
      ></router-link>
    </li>
    <li>
      <router-link
        to="/search"
        uk-icon="icon: search; ratio: 2"
        uk-tooltip="title: 検索; pos: right"
      ></router-link>
    </li>
    <li class="uk-inline">
      <router-link
        to="/notifications"
        uk-icon="icon: bell; ratio: 2"
        uk-tooltip="title: 通知; pos: right"
      ></router-link>
      <span
        class="uk-badge uk-position-top-right uk-margin-small-top"
        v-if="unreadNotificationCount"
      >
        {{ unreadNotificationCount }}
      </span>
    </li>
    <li>
      <router-link
        to="/messages"
        uk-icon="icon: mail; ratio: 2"
        uk-tooltip="title: メッセージ; pos: right"
      ></router-link>
    </li>
    <li>
      <router-link
        to="/profile"
        uk-icon="icon: user; ratio: 2"
        uk-tooltip="title: プロフィール; pos: right"
      ></router-link>
    </li>
    <li>
      <a
        @click="logout"
        uk-icon="icon: sign-out; ratio: 2"
        uk-tooltip="title: ログアウト; pos: right"
      ></a>
    </li>
  </ul>
</template>

<script>
import UIkit from "uikit";
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

export default {
  setup() {
    const store = useStore();
    const router = useRouter();

    const logout = () => {
      store
        .dispatch("logout")
        .then(() => {
          router.push("/login");
        })
        .catch((error) => {
          UIkit.notification(error.response.data.error.message, {
            status: "danger",
          });
        });
    };

    const unreadNotificationCount = computed(() => {
      return store.state.unreadNotificationCount;
    });

    return {
      logout,
      unreadNotificationCount,
    };
  },
};
</script>
