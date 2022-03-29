<template>
  <div class="uk-margin-right">
    <h3 class="uk-margin-top">検索</h3>
    <div class="uk-inline uk-margin-bottom uk-width-1-1">
      <div class="uk-form-custom uk-width-expand">
        <span class="uk-form-icon" uk-icon="search"></span>
        <input
          class="uk-input"
          type="text"
          placeholder="キーワード検索"
          v-model="query"
          @keypress.prevent.enter.exact="enableSubmit"
          @keyup.prevent.enter.exact="submit"
        />
      </div>
    </div>
    <div>
      <ul uk-tab class="uk-child-width-expand">
        <li :class="{ 'uk-active': tab !== 'users' }">
          <router-link
            :to="{
              path: '/search',
              query: {
                q: query,
                type: 'posts',
              },
            }"
            >ツイート</router-link
          >
        </li>
        <li :class="{ 'uk-active': tab === 'users' }">
          <router-link
            :to="{
              path: '/search',
              query: {
                q: query,
                type: 'users',
              },
            }"
            >アカウント</router-link
          >
        </li>
      </ul>
      <div v-if="tab === 'users'">
        <user-panel
          v-for="user in users"
          :key="user._id"
          :user="user"
        ></user-panel>
      </div>
      <div v-else>
        <post-panel
          v-for="post in posts"
          :key="post._id"
          :post="post"
        ></post-panel>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import PostPanel from "@/components/PostPanel.vue";
import UserPanel from "@/components/UserPanel.vue";

export default {
  components: {
    PostPanel,
    UserPanel,
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const query = ref("");
    const tab = ref("");
    const canSubmit = ref(false);

    const enableSubmit = () => {
      canSubmit.value = true;
    };

    const _search = () => {
      const action = tab.value === "users" ? "searchUsers" : "searchPosts";
      store.dispatch(action, { query: query.value });
    };

    const submit = () => {
      if (!canSubmit.value) {
        return;
      }
      _search();
      canSubmit.value = false;
    };

    const posts = computed(() => store.state.search.posts);
    const users = computed(() => store.state.search.users);

    watch(
      () => route.query,
      (newQuery) => {
        query.value = newQuery.q;
        tab.value = newQuery.type ? newQuery.type : "posts";
        _search();
      },
      {
        immediate: true,
      }
    );

    return {
      query,
      tab,
      posts,
      users,
      enableSubmit,
      submit,
    };
  },
};
</script>
