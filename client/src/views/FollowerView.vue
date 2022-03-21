<template>
  <div class="uk-margin-right">
    <div class="uk-margin-top uk-margin-bottom">
      <div class="uk-text-bold">{{ user.display_name }}</div>
      <div class="uk-text-muted uk-text-small">@{{ user.username }}</div>
    </div>
    <div>
      <ul uk-tab class="uk-child-width-expand">
        <li :class="{ 'uk-active': isFollowers }">
          <router-link :to="'/profile/' + username + '/followers'"
            >フォロワー</router-link
          >
        </li>
        <li :class="{ 'uk-active': !isFollowers }">
          <router-link :to="'/profile/' + username + '/following'"
            >フォロー中</router-link
          >
        </li>
      </ul>
    </div>
    <div>
      <user-panel
        v-for="user in users"
        :key="user._id"
        :user="user"
      ></user-panel>
    </div>
  </div>
</template>

<script>
import { computed, watch } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import UserPanel from "@/components/UserPanel.vue";

export default {
  components: {
    UserPanel,
  },
  setup() {
    const route = useRoute();
    const store = useStore();
    let isFollowers = route.meta.followers;
    const username = route.params.username;
    const user = computed(() => store.state.profile.user);

    watch(
      () => route.meta.followers,
      async () => {
        isFollowers = route.meta.followers;
        if (isFollowers) {
          store.dispatch("loadFollowers", { username });
        } else {
          store.dispatch("loadFollowingUsers", { username });
        }
        store.dispatch("loadProfileUser", { username });
      },
      {
        immediate: true,
      }
    );

    const users = computed(() => store.state.profile.users);
    return {
      isFollowers,
      user,
      users,
      username,
    };
  },
};
</script>
