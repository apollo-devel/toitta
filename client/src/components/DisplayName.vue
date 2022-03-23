<template>
  <div class="uk-text-bold">
    <router-link :to="'/profile/' + user.username" class="uk-link-text">
      {{ user.display_name }}
    </router-link>
  </div>
</template>

<script>
export default {
  props: {
    user: Object,
  },
};
</script>
