<template>
  <div class="uk-margin-right">
    <div class="uk-margin-top uk-margin-bottom">
      <div class="uk-text-bold">
        <router-link :to="'/profile/' + user.username" class="uk-link-text">
          {{ user.display_name }}
        </router-link>
      </div>
      <div class="uk-text-muted uk-text-small">
        <router-link :to="'/profile/' + user.username" class="uk-link-text">
          @{{ user.username }}
        </router-link>
      </div>
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
      (followers) => {
        if (followers === undefined) {
          // /profile/XXXX/followers 等の遷移で反応することがあるため回避
          return;
        }
        isFollowers = followers;
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
