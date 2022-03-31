<template>
  <div class="uk-margin-right">
    <div class="uk-flex uk-flex-row uk-flex-middle">
      <h3 class="uk-margin-top">メッセージ</h3>
      <span class="uk-flex-1"></span>
      <span uk-icon="plus" class="new-chat"></span>
    </div>
    <div>
      <div class="uk-flex uk-flex-row uk-flex-middle">
        <div
          class="image-container uk-position-relative uk-margin-small-right uk-flex uk-flex-center multi"
        >
          <img
            class="avatar uk-position-absolute"
            src="https://ui-avatars.com/api/?name=?"
          />
          <img
            class="avatar uk-position-absolute"
            src="https://ui-avatars.com/api/?name=?"
          />
        </div>
        <div class="uk-flex-1 uk-flex uk-flex-column uk-width-expand">
          <div class="uk-text-bold uk-text-truncate uk-margin-right">
            チャット名
          </div>
          <div
            class="uk-text-small uk-text-muted uk-text-truncate uk-margin-right"
          >
            最新のチャット
          </div>
        </div>
      </div>
      <hr />
      <div class="uk-flex uk-flex-row uk-flex-middle">
        <div
          class="image-container uk-position-relative uk-margin-small-right uk-flex uk-flex-center"
        >
          <img class="avatar" src="https://ui-avatars.com/api/?name=?" />
        </div>
        <div class="uk-flex-1 uk-flex uk-flex-column uk-width-expand">
          <div class="uk-text-bold uk-text-truncate uk-margin-right">
            チャット名 チャット名 チャット名 チャット名 チャット名 チャット名
            チャット名 チャット名 チャット名 チャット名 チャット名 チャット名
          </div>
          <div
            class="uk-text-small uk-text-muted uk-text-truncate uk-margin-right"
          >
            最新のチャット 最新のチャット 最新のチャット 最新のチャット
            最新のチャット 最新のチャット 最新のチャット 最新のチャット
          </div>
        </div>
      </div>
      <hr />
    </div>
  </div>
</template>

<style scoped>
.image-container {
  width: 40px;
  height: 40px;
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid white;
}

.multi .avatar {
  height: 65%;
  width: 65%;
  bottom: 0;
  margin: 0;
}

.multi .avatar:first-of-type {
  top: 0;
  right: 0;
}

.new-chat {
  cursor: pointer;
}
</style>