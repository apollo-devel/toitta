<template>
  <div class="uk-margin-right">
    <div>
      <h3 class="uk-margin-top">新しいメッセージ</h3>
    </div>
    <div class="search uk-search uk-search-default uk-width-expand">
      <span uk-search-icon></span>
      <input
        type="search"
        class="uk-search-input"
        placeholder="ユーザーを検索"
        v-model="query"
        @keyup="onKeyUp"
      />
    </div>
    <div class="selected uk-padding-small">
      <span
        class="uk-label"
        v-for="selected in selectedUsers"
        :key="selected._id"
      >
        {{ selected.display_name }}
        <button class="uk-close" uk-close @click="remove(selected)"></button>
      </span>
    </div>
    <div class="uk-text-center">
      <button
        class="uk-button uk-button-primary"
        :disabled="isInvalid"
        @click="submit"
      >
        チャットを作成
      </button>
    </div>
    <hr />
    <div>
      <user-panel
        v-for="user in users"
        :user="user"
        :key="user._id"
        :disableLink="true"
        @click="select(user)"
        class="clickable"
      ></user-panel>
    </div>
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import UserPanel from "@/components/UserPanel.vue";

export default {
  components: {
    UserPanel,
  },
  setup() {
    const store = useStore();
    store.dispatch("clearUsersForChat");
    const query = ref("");

    let timer;
    const onKeyUp = () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        if (query.value.trim()) {
          store.dispatch("searchUsersForChat", { query: query.value });
        }
      }, 1000);
    };

    const selectedUsers = ref([]);

    const users = computed(() => {
      const ids = selectedUsers.value.map((u) => {
        return u._id;
      });
      ids.push(store.state.userLoggedIn._id);
      return store.state.chat.users.filter((u) => !ids.includes(u._id));
    });

    const select = (user) => {
      selectedUsers.value.push(user);
    };

    const remove = (user) => {
      const idx = selectedUsers.value.findIndex((u) => u._id === user._id);
      if (idx > -1) {
        selectedUsers.value.splice(idx, 1);
      }
    };

    const isInvalid = computed(() => selectedUsers.value.length <= 0);

    const router = useRouter();
    const submit = () => {
      const ids = [store.state.userLoggedIn._id];
      selectedUsers.value.forEach((u) => ids.push(u._id));
      store.dispatch("createChat", { users: ids }).then((resp) => {
        router.push({
          name: "chat",
          params: {
            chatId: resp._id,
          },
        });
      });
    };

    return {
      query,
      users,
      selectedUsers,
      onKeyUp,
      select,
      remove,
      isInvalid,
      submit,
    };
  },
};
</script>

<style scoped>
.selected {
  min-height: 50px;
}

.search input {
  border: none;
  border-bottom: 1px solid #e5e5e5;
}

.selected .uk-label {
  height: 30px;
  padding-top: 9px;
  margin: 3px;
}

.uk-close {
  color: white;
}

.clickable {
  cursor: pointer;
}
</style>