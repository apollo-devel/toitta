<template>
  <div class="uk-grid uk-height-1-1">
    <div class="uk-width-auto">
      <side-nav></side-nav>
    </div>
    <div class="uk-width-expand uk-height-1-1">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import SideNav from "@/components/SideNav.vue";

export default {
  components: {
    SideNav,
  },
};
</script>
