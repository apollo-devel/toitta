<template>
  <router-link
    :to="'/profile/' + user.username"
    :class="{ 'large-link': size === 'large' }"
    v-if="!disableLink"
  >
    <img
      :src="url"
      class="uk-border-circle avatar"
      :class="{ large: size === 'large', small: size === 'small' }"
    />
  </router-link>
  <img
    v-else
    :src="url"
    class="uk-border-circle avatar"
    :class="{ large: size === 'large', small: size === 'small' }"
  />
</template>

<script>
import { computed } from "vue";

export default {
  props: {
    user: Object,
    size: String,
    disableLink: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const imageUrl = (user) => {
      if (!user || !user.display_name) {
        return "https://ui-avatars.com/api/?name=?";
      }

      if (!user.profile_pic) {
        return `https://ui-avatars.com/api/?name=${user.display_name}`;
      }
      return user.profile_pic;
    };
    const url = computed(() => imageUrl(props.user));
    return {
      url,
    };
  },
};
</script>

<style scoped>
.avatar {
  max-width: 50px;
  width: 50px;
  height: 50px;
}

.avatar.large {
  max-width: 132px;
  width: 132px;
  height: 132px;
  border: 4px solid #fff;
}

.avatar.small {
  max-width: 24px;
  width: 24px;
  height: 24px;
}

.large-link {
  z-index: 1000;
}
</style>