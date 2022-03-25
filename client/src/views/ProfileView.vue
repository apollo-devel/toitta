<template>
  <div class="uk-width-1-1 uk-position-relative">
    <h3 class="uk-margin-small-top uk-margin-small-bottom">
      {{ user.username }}
    </h3>
    <div class="cover uk-margin-right"></div>
    <avatar-pic
      :user="user"
      size="large"
      class="uk-position-absolute uk-margin-small-left large-avatar"
    ></avatar-pic>
    <div class="uk-width-1-1 uk-position-absolute" v-if="user._id">
      <div
        class="uk-flex uk-flex-row uk-flex-top uk-margin-right uk-margin-small-top buttons"
      >
        <div class="uk-flex-1"></div>
        <button
          v-if="isMe"
          class="uk-button uk-button-default uk-button-small uk-text-bold"
        >
          プロフィールを編集
        </button>
        <button
          v-else
          class="follow uk-button uk-button-small uk-text-bold"
          :class="isFollowing ? 'uk-button-default' : 'uk-button-secondary'"
          @click="onFollowClick"
        >
          {{ isFollowing ? "フォロー中" : "フォロー" }}
        </button>
      </div>
      <div class="uk-flex uk-flex-column uk-flex-left uk-margin-small-left">
        <div class="uk-text-large uk-text-bold">{{ user.display_name }}</div>
        <div>@{{ user.username }}</div>
        <div class="uk-margin-small-top">{{ user.description }}</div>
        <div class="uk-margin-small-top">
          <router-link
            :to="'/profile/' + user.username + '/following'"
            class="uk-link-text uk-margin-right"
          >
            <span class="uk-text-bold">{{
              user.following ? user.following.length : 0
            }}</span>
            <span>フォロー中</span>
          </router-link>
          <router-link
            :to="'/profile/' + user.username + '/followers'"
            class="uk-link-text"
          >
            <span class="uk-text-bold">{{
              user.followers ? user.followers.length : 0
            }}</span>
            <span>フォロワー</span>
          </router-link>
        </div>
      </div>
      <div class="uk-margin-top uk-margin-right">
        <ul class="uk-child-width-expand" ref="tabs" uk-tab>
          <li :class="{ 'uk-active': tab === 'tweets' }">
            <router-link :to="'/profile/' + user.username">
              ツイート
            </router-link>
          </li>
          <li :class="{ 'uk-active': tab === 'tweetsAndReplies' }">
            <router-link
              :to="'/profile/' + user.username + '/tweets_and_replies'"
            >
              ツイートと返信
            </router-link>
          </li>
          <li :class="{ 'uk-active': tab === 'likes' }">
            <router-link :to="'/profile/' + user.username + '/likes'">
              いいね
            </router-link>
          </li>
        </ul>
      </div>
      <div>
        <post-panel
          v-for="post in posts"
          :key="post._id"
          :post="post"
        ></post-panel>
      </div>
    </div>
    <div class="uk-position-absolute error-message" v-else>
      <h3>ユーザーが存在しません</h3>
    </div>
  </div>
</template>

<script>
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import AvatarPic from "@/components/AvatarPic.vue";
import PostPanel from "@/components/PostPanel.vue";

export default {
  components: {
    AvatarPic,
    PostPanel,
  },
  setup() {
    const route = useRoute();
    const store = useStore();

    let tab = computed(() => route.meta.tab);
    let posts = computed(() => store.state.profile[tab.value]);
    const isMe = ref(false);
    const isFollowing = computed(
      () =>
        store.state.userLoggedIn.following &&
        store.state.userLoggedIn.following.includes(
          store.state.profile.user._id
        )
    );
    const user = computed(() => store.state.profile.user);

    watch(
      () => [route.params.username, route.meta.tab],
      () => {
        const username = route.params.username
          ? route.params.username
          : store.state.userLoggedIn.username;
        store
          .dispatch("loadProfileUser", { username })
          .then(() => {
            isMe.value = username === store.state.userLoggedIn.username;
            store.dispatch("loadProfilePosts", { username, tab: tab.value });
          })
          .catch(() => {
            // noop
          });
      },
      {
        immediate: true,
      }
    );

    const onFollowClick = () => {
      if (isFollowing.value) {
        store
          .dispatch("unfollowUser", { username: user.value.username })
          .then(() =>
            store.dispatch("loadProfileUser", { username: user.value.username })
          );
      } else {
        store
          .dispatch("followUser", { username: user.value.username })
          .then(() =>
            store.dispatch("loadProfileUser", { username: user.value.username })
          );
      }
    };

    return {
      isMe,
      isFollowing,
      user,
      tab,
      posts,
      onFollowClick,
    };
  },
};
</script>

<style scoped>
.cover {
  background-color: lightslategray;
  height: 180px;
}

.large-avatar {
  bottom: -66px;
}

.buttons {
  height: 60px;
}

.error-message {
  margin-top: 30px;
  margin-left: 132px;
}
</style>