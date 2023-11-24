<script setup>
import { ref } from "vue";
import { invoke } from "@tauri-apps/api/primitives";

const state = ref(-1);
</script>

<template>

    <div v-if="state==-1">
        <form id="find_match" @submit.prevent="state=0">
            <textarea id="matching_desc"/>
            <button id="sub_match">Find Match</button>
        </form>
    </div>
    <div v-if="state==1">
        <div class="match_title">
            <p>Your Match</p>
        </div>
       <div id="top_mcard" class="match_card">
            <div class = "report-card-head">
                <img class="card_avatar" src="../assets/dog.jpg" alt="Avatar">
                <p>Zephyr</p>
            </div>
            <p id="carddesc"> <b>"</b>You are 98% matched because you are both a little bit introverted, gentle with people around you. Hint: you may have a lot of common childhood memories!"</p>
       </div>
    </div>

    <div>

    </div>
    
    <img v-if="state==0" id="matching_anim" @animationend="state=1" src="../assets/matching.gif"> 

</template>