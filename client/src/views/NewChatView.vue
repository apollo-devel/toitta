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
      />
    </div>
    <div class="selected uk-padding-small">
      <span class="uk-label">
        ユーザー１
        <button class="uk-close" uk-close></button>
      </span>
      <span class="uk-label">
        ユーザー１
        <button class="uk-close" uk-close></button>
      </span>
      <span class="uk-label">
        ユーザー１
        <button class="uk-close" uk-close></button>
      </span>
      <span class="uk-label">
        ユーザー１
        <button class="uk-close" uk-close></button>
      </span>
      <span class="uk-label">
        ユーザー１
        <button class="uk-close" uk-close></button>
      </span>
      <span class="uk-label">
        ユーザー１
        <button class="uk-close" uk-close></button>
      </span>
      <span class="uk-label">
        ユーザー１
        <button class="uk-close" uk-close></button>
      </span>
      <span class="uk-label">
        ユーザー１
        <button class="uk-close" uk-close></button>
      </span>
    </div>
    <div class="uk-text-center">
      <button class="uk-button uk-button-primary">チャットを作成</button>
    </div>
    <hr />
    <div>
      <user-panel :user="user" disableLink="true"></user-panel>
      <user-panel :user="user" disableLink="true"></user-panel>
    </div>
  </div>
</template>

<script>
import UserPanel from "@/components/UserPanel.vue";

export default {
  components: {
    UserPanel,
  },
  setup() {
    const user = {
      username: "ユーザー名",
      display_name: "表示名",
    };
    return {
      user,
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
</style>