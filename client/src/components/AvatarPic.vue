<template>
  <router-link
    :to="'/profile/' + user.username"
    :class="{ 'large-link': size === 'large' }"
  >
    <img
      :src="url"
      class="uk-border-circle avatar"
      :class="{ large: size === 'large' }"
    />
  </router-link>
</template>

<script>
import { computed } from "vue";

export default {
  props: {
    user: Object,
    size: String,
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

.large-link {
  z-index: 20000;
}
</style>