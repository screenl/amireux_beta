<script setup>
import { onMounted, ref } from "vue";
const expand = ref(false);
const emit = defineEmits(['goToChat','goToAnalysis','goToMatch']);

</script>

<template>
    <button class="return_button" @click="expand=!expand"></button>
    <div class="topnav">
        <div class = "return" > <p>☰</p> </div>
        <div class = "rtopnav"><img class="amir_logo" src = "../assets/Amireux.svg"/></div>
    </div>
    <div class="menu" v-if="expand">
        <div class="mitem" @click="emit('goToChat')">Chat with AI</div>
        <div class="mitem" @click="emit('goToAnalysis')">View Personality Report</div>
        <div class="mitem" @click="emit('goToMatch')">Matching</div>
    </div>

</template>