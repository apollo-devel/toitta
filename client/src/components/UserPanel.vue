<template>
  <div>
    <div class="uk-flex uk-flex-top">
      <avatar-pic :user="user"></avatar-pic>
      <div
        class="uk-flex uk-flex-left uk-flex-column uk-flex-1 uk-margin-small-left"
      >
        <div class="uk-flex uk-flex-row uk-flex-center">
          <div class="uk-flex-1">
            <display-name :user="user"></display-name>
            <div>
              <username-link :user="user"></username-link>
              <span class="uk-label" v-if="isFollowed">
                フォローされています
              </span>
            </div>
          </div>
          <div>
            <button
              v-if="!isMe"
              class="uk-button uk-button-small"
              :class="isFollowing ? 'uk-button-default' : 'uk-button-secondary'"
              @click="onFollowClick"
            >
              {{ isFollowing ? "フォロー中" : "フォロー" }}
            </button>
          </div>
        </div>
        <div class="uk-margin-small-top">
          {{ user.description }}
        </div>
      </div>
    </div>
    <hr />
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";

import AvatarPic from "@/components/AvatarPic.vue";
import DisplayName from "@/components/DisplayName.vue";
import UsernameLink from "@/components/UsernameLink.vue";

export default {
  components: {
    AvatarPic,
    DisplayName,
    UsernameLink,
  },
  props: {
    user: Object,
  },
  setup(props) {
    const store = useStore();

    const isFollowing = computed(() =>
      store.state.userLoggedIn.following.includes(props.user._id)
    );
    const isFollowed = computed(() =>
      store.state.userLoggedIn.followers.includes(props.user._id)
    );

    const username = ref(props.user.username);

    const isMe = props.user._id === store.state.userLoggedIn._id;

    const onFollowClick = () => {
      if (isFollowing.value) {
        store.dispatch("unfollowUser", { username: username.value });
      } else {
        store.dispatch("followUser", { username: username.value });
      }
    };

    return {
      isMe,
      isFollowing,
      isFollowed,
      onFollowClick,
    };
  },
};
</script>