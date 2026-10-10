import { initializeApp } from "https://www.gstatic.com/firebasejs/12.19.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.19.0/firebase-analytics.js";
import {
  getAuth,
  GoogleAuthProvider,
  onAuthStateChanged,
  signInWithCredential,
  signOut as firebaseSignOut
} from "https://www.gstatic.com/firebasejs/12.19.0/firebase-auth.js";
import {
  getFirestore,
  doc,
  getDoc,
  setDoc,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/12.19.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyCYrJXVlMv-bkH5AKycARV7-C7veYxz7hc",
  authDomain: "ruhi-wholesale.firebaseapp.com",
  projectId: "ruhi-wholesale",
  storageBucket: "ruhi-wholesale.firebasestorage.app",
  messagingSenderId: "1060732686750",
  appId: "1:1060732686750:web:abf8e2b588802fdc3a068f",
  measurementId: "G-TM8YF30RMH"
};

const GOOGLE_CLIENT_ID = "900341067132-1s8aonb1dhm4vu91pbpnpejjdk3uh6p3.apps.googleusercontent.com";
const CART_KEY = "ruhi_wholesellers_cart_v4";
const GUEST_CART_KEY = "ruhi_guest_cart_v1";
const USER_KEY = "ruhi_user";
const app = initializeApp(firebaseConfig);
try { getAnalytics(app); } catch (error) { console.warn("Firebase Analytics unavailable:", error); }
const auth = getAuth(app);
const db = getFirestore(app);
const googleProvider = new GoogleAuthProvider();

function normalizeCart(value) {
  try {
    const parsed = Array.isArray(value) ? value : JSON.parse(value || "[]");
    if (!Array.isArray(parsed)) return [];
    return parsed
      .filter(item => item && typeof item.id === "string" && Number.isFinite(Number(item.qty)) && Number(item.qty) > 0)
      .map(item => ({ id: item.id, qty: Math.max(1, Math.floor(Number(item.qty))) }));
  } catch (_) { return []; }
}

function readLocalCart(key = CART_KEY) {
  try { return normalizeCart(localStorage.getItem(key)); } catch (_) { return []; }
}

function writeLocalCart(cart, key = CART_KEY) {
  try { localStorage.setItem(key, JSON.stringify(normalizeCart(cart))); } catch (_) {}
}

function mergeCarts(first, second) {
  const merged = normalizeCart(first).map(item => ({ ...item }));
  normalizeCart(second).forEach(item => {
    const existing = merged.find(x => x.id === item.id);
    if (existing) existing.qty += item.qty;
    else merged.push({ ...item });
  });
  return merged;
}

function userCartRef(email) {
  const normalizedEmail = String(email || "").trim().toLowerCase();
  return normalizedEmail ? doc(db, "users", normalizedEmail, "cart", "current") : null;
}

function saveUserLocally(user) {
  if (!user?.email) return;
  const data = {
    name: user.displayName || user.name || user.email,
    email: user.email,
    picture: user.photoURL || user.picture || ""
  };
  try { localStorage.setItem(USER_KEY, JSON.stringify(data)); } catch (_) {}
  window.RUHI_INDEX_SESSION?.setUser?.(data);
}

async function loadCloudCart(email) {
  const ref = userCartRef(email);
  if (!ref) return [];
  const snap = await getDoc(ref);
  if (!snap.exists()) return [];
  return normalizeCart(snap.data()?.items);
}

async function saveCloudCart(email, cart) {
  const ref = userCartRef(email);
  if (!ref) return;
  await setDoc(ref, {
    items: normalizeCart(cart),
    updatedAt: serverTimestamp()
  }, { merge: true });
}

function publishCart(cart) {
  const normalized = normalizeCart(cart);
  writeLocalCart(normalized, CART_KEY);
  window.dispatchEvent(new CustomEvent("ruhi:cart-updated", { detail: { cart: normalized } }));
  window.RUHI_INDEX_SESSION?.setCart?.(normalized);
}

async function syncAuthenticatedCart(firebaseUser) {
  if (!firebaseUser?.email) return;
  const email = firebaseUser.email.trim().toLowerCase();
  saveUserLocally(firebaseUser);

  try {
    const cloudCart = await loadCloudCart(email);
    const localAccountCart = readLocalCart("ruhi_cart_" + encodeURIComponent(email));
    const guestCart = readLocalCart(GUEST_CART_KEY);
    const legacyCart = readLocalCart(CART_KEY);
    const hasGuest = guestCart.length > 0;
    const localCart = localAccountCart.length ? localAccountCart : (!hasGuest ? legacyCart : []);
    const merged = mergeCarts(cloudCart, mergeCarts(localCart, guestCart));

    writeLocalCart(merged, "ruhi_cart_" + encodeURIComponent(email));
    writeLocalCart(merged, CART_KEY);
    try {
      localStorage.removeItem(GUEST_CART_KEY);
    } catch (_) {}

    publishCart(merged);
    await saveCloudCart(email, merged);
  } catch (error) {
    console.error("Ruhi Firebase cart sync failed:", error);
    publishCart(readLocalCart("ruhi_cart_" + encodeURIComponent(email)));
  }
}

async function syncCurrentCartToCloud(cart) {
  const firebaseUser = auth.currentUser;
  if (!firebaseUser?.email) return;
  const normalized = normalizeCart(cart);
  writeLocalCart(normalized, "ruhi_cart_" + encodeURIComponent(firebaseUser.email.trim().toLowerCase()));
  try { await saveCloudCart(firebaseUser.email, normalized); }
  catch (error) { console.error("Ruhi Firebase cart save failed:", error); }
}

async function acceptGoogleCredential(credential) {
  if (!credential) return false;
  try {
    const firebaseCredential = GoogleAuthProvider.credential(credential);
    await signInWithCredential(auth, firebaseCredential);
    return true;
  } catch (error) {
    console.error("Firebase Google authentication failed:", error);
    const status = document.getElementById("accountStatus");
    if (status) status.textContent = "Google sign-in could not be completed. Please try again.";
    return false;
  }
}

async function signOut() {
  try { await firebaseSignOut(auth); }
  catch (error) { console.error("Firebase sign-out failed:", error); }
}

window.RUHI_FIREBASE = {
  auth,
  db,
  GOOGLE_CLIENT_ID,
  saveCart: syncCurrentCartToCloud,
  loadCloudCart,
  saveCloudCart,
  acceptGoogleCredential,
  signOut
};

onAuthStateChanged(auth, async firebaseUser => {
  if (firebaseUser) {
    await syncAuthenticatedCart(firebaseUser);
  }
  if (typeof window.__resolveRuhiFirebase === "function") {
    window.__resolveRuhiFirebase();
    window.__resolveRuhiFirebase = null;
  }
});
