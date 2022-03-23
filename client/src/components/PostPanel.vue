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
        <div v-if="isReply">
          @{{ displayPost.reply_to.posted_by.username }} へ返信
        </div>
        <div class="uk-flex uk-margin-small-top">
          {{ displayPost.content }}
        </div>
        <div class="uk-flex uk-flex-between uk-margin-small-top">
          <span class="uk-flex-1 reply">
            <span uk-icon="comment" @click="onReplyClick"></span>
          </span>
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
import { computed } from "vue";
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
  setup(props, context) {
    const store = useStore();

    const isRetweet = Boolean(props.post && props.post.retweeted_post);
    const isReply = Boolean(props.post && props.post.reply_to);
    const displayPost = computed(() =>
      isRetweet ? props.post.retweeted_post : props.post
    );

    const onLikeClick = () => {
      if (displayPost.value.liking) {
        store.dispatch("unlikePost", { post: displayPost.value });
      } else {
        store.dispatch("likePost", { post: displayPost.value });
      }
    };

    const onRetweetClick = () => {
      if (displayPost.value.retweeting) {
        store.dispatch("unretweetPost", { post: displayPost.value });
      } else {
        store.dispatch("retweetPost", { post: displayPost.value });
      }
    };

    const onReplyClick = () => {
      context.emit("clickReply", displayPost.value);
    };

    return {
      isRetweet,
      isReply,
      displayPost,
      onLikeClick,
      onRetweetClick,
      onReplyClick,
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
.retweet,
.reply {
  cursor: pointer;
}
</style>