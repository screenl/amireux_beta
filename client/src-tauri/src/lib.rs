// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
use std::{sync::{Arc,Mutex}, collections::HashMap};
use serde::Deserialize;
use tauri::State;
use reqwest::{self, Client};
const SERVER: &'static str = "Your server here";
#[derive(Deserialize)]
struct ReturnMsg {
    ai_response: String,
}

#[derive(Deserialize)]
struct AnalysisMsg {
    message: String,
}
async fn get_ai_resp(message: &str, client: &Arc<Client>) -> Result<String,Box<dyn std::error::Error>> {
    let resp = client.post(format!("{SERVER}/send_message_to_character_ai"))
        .json(&HashMap::from([("message",message)]))
        .send().await?;
    println!("hi?");
    Ok(resp.json::<ReturnMsg>().await?.ai_response)
}

async fn signin(name: &str, client: &Arc<Client>) -> Result<(),Box<dyn std::error::Error>>{
    client.post(format!("{SERVER}/sign_in"))
        .json(&HashMap::from([("username",name)]))
        .send().await?;
    Ok(())
}

#[tauri::command]
async fn sign_in(name: &str, sess: State<'_,UserSession>) -> Result<String,()>{
    let client = &(sess.session);
    let uname = sess.name.as_ref();
    uname.lock().map_err(|_| ())?.clear();
    uname.lock().map_err(|_| ())?.push_str(name);
    signin(name, client).await.map_err(|_| ())?;
    *(sess.signed_in.lock().map_err(|_| ())?) = true;
    Ok("".to_string())
}

#[tauri::command]
fn get_username(sess: State<'_,UserSession>) -> String{
    println!("{}",sess.name.as_ref().lock().unwrap());
    sess.name.as_ref().lock().unwrap().clone()
}

#[tauri::command]
async fn get_analysis(sess: State<'_,UserSession>) -> Result<String,()> { 
    let client = &(sess.session);
    if !(*(sess.signed_in.lock().map_err(|_| ())?)){    
        println!("login first!");
        return Err(());
    }
    let resp = client.get(format!("{SERVER}/get_analysis")).send().await.map_err(|_| ())?;
    Ok(resp.json::<AnalysisMsg>().await.unwrap().message)
}

#[tauri::command]
async fn greet(name: &str, sess: State<'_,UserSession>) -> Result<String, ()>{
    let client = &(sess.session);
    if !(*(sess.signed_in.lock().map_err(|_| ())?)){
        println!("login first!");
        return Err(());
    }
    let t = get_ai_resp(name,client).await.unwrap();
    let msgs = sess.messages.as_ref();
    msgs.lock().map_err(|_| ())?.push((0,name.to_string()));
    msgs.lock().map_err(|_| ())?.push((1,t.clone()));
    println!("{}",t);
    Ok(t)
}


struct UserSession {
    name: Arc<Mutex<String>>,
    signed_in: Mutex<bool>,
    messages: Arc<Mutex<Vec<(u8,String)>>>,
    session: Arc<reqwest::Client>
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let m = UserSession{
        name: Arc::new(Mutex::new(String::from("coltrane"))),
        signed_in: Mutex::new(false),
        messages: Arc::new(Mutex::new(Vec::new())),
        session: Arc::new(reqwest::Client::builder().cookie_store(true).build().unwrap())
    };
    tauri::Builder::default()
        .manage(m)
        .plugin(tauri_plugin_window::init())
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![greet,get_username,get_analysis,sign_in])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
