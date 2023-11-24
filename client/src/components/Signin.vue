<script setup>
    import { onMounted, ref } from "vue";
    import { invoke } from "@tauri-apps/api/primitives";
    const username = ref("");
    const signedin = ref(false)
    const emit = defineEmits(['signed']);
    async function signin(){
        await invoke("sign_in",{name: username.value});
        signedin.value = true;
        emit('signed');
    }
</script>

<template>
    <form class="login" @submit.prevent="signin">

        <h3>Please enter a username:</h3>
        <input id="unameinput" v-model="username" />
        <button type="submit">Go</button>
    </form>
</template>