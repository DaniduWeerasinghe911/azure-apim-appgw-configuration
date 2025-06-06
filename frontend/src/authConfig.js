// MSAL.js config for Azure AD login
export const msalConfig = {
  auth: {
    clientId: '84930e22-733c-4d05-8f66-8c523095a89a',
    authority: "https://login.microsoftonline.com/78be17d2-30b3-4f7d-91c9-236348af26d9",
    redirectUri: "http://localhost:5176/",
  },
  cache: {
    cacheLocation: "localStorage",
    storeAuthStateInCookie: false,
  },
};
export const loginRequest = {
  scopes: ["api://84930e22-733c-4d05-8f66-8c523095a89a/user_impersonation"]
};
