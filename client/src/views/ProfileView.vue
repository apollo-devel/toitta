<template>
  <div class="uk-width-1-1 uk-position-relative">
    <h3 class="uk-margin-small-top uk-margin-small-bottom">Hoge</h3>
    <div class="cover uk-margin-right"></div>
    <img
      src="https://ui-avatars.com/api/?name=?"
      class="uk-position-absolute uk-border-circle uk-margin-small-left avatar"
    />
    <div class="uk-width-1-1 uk-position-absolute">
      <div
        class="uk-flex uk-flex-row uk-flex-top uk-margin-right uk-margin-small-top buttons"
      >
        <div class="uk-flex-1"></div>
        <button
          class="uk-button uk-button-default uk-button-small uk-text-bold"
        >
          プロフィールを編集
        </button>
      </div>
      <div class="uk-flex uk-flex-column uk-flex-left uk-margin-small-left">
        <div class="uk-text-large uk-text-bold">Hoge</div>
        <div>@hoge</div>
        <div class="uk-margin-small-top">あいうえお</div>
        <div class="uk-margin-small-top">
          <span class="uk-text-bold">100</span>
          <span class="uk-margin-right">フォロー中</span>
          <span class="uk-text-bold">50</span>
          <span>フォロワー</span>
        </div>
      </div>
      <div class="uk-margin-top uk-margin-right">
        <ul class="uk-child-width-expand" ref="tabs" uk-tab uk-switcher>
          <li><a>ツイート</a></li>
          <li><a>ツイートと返信</a></li>
          <li><a>いいね</a></li>
        </ul>
        <ul class="uk-switcher">
          <div>ツイートです</div>
          <div>ツイートと返信です</div>
          <div>いいねです</div>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import UIkit from "uikit";
import { ref, onMounted } from "vue";

export default {
  setup() {
    const tabs = ref(null);
    onMounted(() => {
      UIkit.tab(tabs);
    });
  },
};
</script>

<style scoped>
.cover {
  background-color: lightslategray;
  height: 180px;
}

.avatar {
  width: 132px;
  height: 132px;
  bottom: -66px;
  border: 4px solid #fff;
}

.buttons {
  height: 60px;
}
</style>