<template>
    <div>
        <div class="uk-flex uk-flex-top">
            <img src="https://ui-avatars.com/api/?name=あぽろ" class="uk-border-circle avatar">
            <textarea placeholder="いまどうしてる？" class="uk-textarea uk-margin-left textarea"></textarea>
        </div>
        <div class="uk-flex uk-flex-right">
            <button class="uk-button uk-button-primary uk-margin-right">ツイートする</button>
        </div>
    </div>
</template>

<style scoped>
.textarea {
    resize: none;
    border: 0;
    height: 100px;
    margin-top: 5px;
}

.avatar {
    width: 50px;
    height: 50px;
}
</style>