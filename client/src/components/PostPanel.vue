<template>
  <div class="uk-margin-right">
    <div class="uk-margin-small-left uk-margin-small-bottom" v-if="isRetweet">
      <router-link
        :to="'/profile/' + post.posted_by.username"
        class="uk-link-text"
      >
        {{ post.posted_by.display_name }}がリツイート
      </router-link>
    </div>
    <div class="uk-flex uk-flex-top">
      <avatar-pic :user="displayPost.posted_by"></avatar-pic>
      <div class="uk-flex uk-flex-left uk-flex-column uk-margin-left uk-flex-1">
        <div class="uk-flex uk-flex-middle uk-flex-row">
          <display-name :user="displayPost.posted_by"></display-name>
          <username-link
            :user="displayPost.posted_by"
            class="uk-margin-small-left"
          ></username-link>
          <span class="uk-margin-small-left uk-text-muted">
            {{ displayPost.created_at }}
          </span>
          <span class="uk-flex-1"></span>
          <span uk-icon="icon: close; ratio: 0.8"></span>
        </div>
        <div class="uk-flex uk-margin-small-top">
          {{ displayPost.content }}
        </div>
        <div class="uk-flex uk-flex-between uk-margin-small-top">
          <span class="uk-flex-1" uk-icon="comment"></span>
          <span
            class="uk-flex-1 retweet"
            :class="{ active: displayPost.retweeting }"
          >
            <span uk-icon="bolt" @click="onRetweetClick"></span>
            <span class="uk-margin-small-left">{{
              displayPost.retweet_count ? displayPost.retweet_count : ""
            }}</span>
          </span>
          <span class="uk-flex-1 like" :class="{ active: displayPost.liking }">
            <span uk-icon="heart" @click="onLikeClick"></span>
            <span class="uk-margin-small-left">{{
              displayPost.like_count ? displayPost.like_count : ""
            }}</span>
          </span>
        </div>
      </div>
    </div>
    <hr />
  </div>
</template>

<script>
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
    post: Object,
  },
  setup(props) {
    const store = useStore();

    const isRetweet = Boolean(props.post.retweeted_post);
    const displayPost = isRetweet ? props.post.retweeted_post : props.post;

    const onLikeClick = () => {
      if (displayPost.liking) {
        store.dispatch("unlikePost", { post: displayPost });
      } else {
        store.dispatch("likePost", { post: displayPost });
      }
    };

    const onRetweetClick = () => {
      if (displayPost.retweeting) {
        store.dispatch("unretweetPost", { post: displayPost });
      } else {
        store.dispatch("retweetPost", { post: displayPost });
      }
    };
    return {
      isRetweet,
      displayPost,
      onLikeClick,
      onRetweetClick,
    };
  },
};
</script>

<style scoped>
.like.active {
  color: red;
}

.retweet.active {
  color: green;
}

.like,
.retweet {
  cursor: pointer;
}
</style>