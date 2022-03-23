<template>
  <div class="uk-text-bold">
    <router-link
      :to="'/profile/' + user.username"
      class="uk-link-text"
      v-if="!disableLink"
    >
      {{ user.display_name }}
    </router-link>
    <span v-else>{{ user.display_name }}</span>
  </div>
</template>

<script>
export default {
  props: {
    user: Object,
    disableLink: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
