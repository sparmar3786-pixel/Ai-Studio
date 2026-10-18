package com.aistudio.charts;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.view.ViewGroup;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.view.Gravity;
import android.view.inputmethod.InputMethodManager;
import android.content.Context;
import android.text.InputType;
import android.view.KeyEvent;
import android.view.inputmethod.EditorInfo;
import android.widget.Toast;
import android.net.Uri;

public class MainActivity extends Activity {
    private WebView webView;
    private SharedPreferences prefs;
    private static final String PREFS = "chart_settings";
    private static final String KEY_BACKEND = "backend_url";

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        prefs = getSharedPreferences(PREFS, MODE_PRIVATE);
        showApp();
        if (prefs.getString(KEY_BACKEND, "").trim().isEmpty()) {
            showBackendDialog(true);
        } else {
            loadCharts();
        }
    }

    private void showApp() {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.rgb(7, 11, 18));
        TextView settings = new TextView(this);
        settings.setText("Ai-Studio Charts     •     Configure Groww backend");
        settings.setTextColor(Color.WHITE);
        settings.setTextSize(14);
        settings.setGravity(Gravity.CENTER_VERTICAL);
        settings.setPadding(16, 12, 16, 12);
        settings.setBackgroundColor(Color.rgb(14, 22, 34));
        settings.setOnClickListener(v -> showBackendDialog(false));
        root.addView(settings, new LinearLayout.LayoutParams(-1, 48));
        webView = new WebView(this);
        WebSettings ws = webView.getSettings();
        ws.setJavaScriptEnabled(true);
        ws.setDomStorageEnabled(true);
        ws.setAllowFileAccess(true);
        ws.setAllowContentAccess(true);
        ws.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        webView.setWebChromeClient(new WebChromeClient());
        root.addView(webView, new LinearLayout.LayoutParams(-1, 0, 1));
        setContentView(root);
    }

    private void loadCharts() {
        String backend = prefs.getString(KEY_BACKEND, "").trim();
        String url = "file:///android_asset/order_flow_footprint_prototype.html";
        if (!backend.isEmpty()) url += "?backend=" + Uri.encode(normalizeBackend(backend));
        webView.loadUrl(url);
    }

    private String normalizeBackend(String value) {
        String v = value.trim();
        if (v.startsWith("https://")) v = "wss://" + v.substring(8);
        else if (v.startsWith("http://")) v = "ws://" + v.substring(7);
        if (!v.startsWith("wss://") && !v.startsWith("ws://")) v = "wss://" + v;
        while (v.endsWith("/")) v = v.substring(0, v.length() - 1);
        if (!v.endsWith("/ws/market")) v += "/ws/market";
        return v;
    }

    private void showBackendDialog(boolean firstRun) {
        EditText input = new EditText(this);
        input.setSingleLine(true);
        input.setTextSize(14);
        input.setHint("https://your-backend-domain");
        input.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_URI);
        input.setText(prefs.getString(KEY_BACKEND, ""));
        new AlertDialog.Builder(this)
            .setTitle("Groww live-data backend")
            .setMessage("Enter your deployed Ai-Studio backend URL. Keep GROWW_ACCESS_TOKEN on the server only; never enter it here. Without a configured backend, the chart stays in WAIT/demo mode.")
            .setView(input)
            .setCancelable(!firstRun)
            .setPositiveButton("Save & connect", (d, which) -> {
                String value = input.getText().toString().trim();
                if (!value.isEmpty()) {
                    if (!(value.startsWith("https://") || value.startsWith("http://") || value.startsWith("wss://") || value.startsWith("ws://"))) {
                        value = "https://" + value;
                    }
                    prefs.edit().putString(KEY_BACKEND, value).apply();
                    loadCharts();
                } else {
                    prefs.edit().remove(KEY_BACKEND).apply();
                    if (firstRun) webView.loadUrl("file:///android_asset/order_flow_footprint_prototype.html");
                }
            })
            .setNegativeButton(firstRun ? "Continue demo" : "Cancel", (d, w) -> {
                if (firstRun) webView.loadUrl("file:///android_asset/order_flow_footprint_prototype.html");
            })
            .setNeutralButton("Clear", (d, w) -> {
                prefs.edit().remove(KEY_BACKEND).apply();
                webView.loadUrl("file:///android_asset/order_flow_footprint_prototype.html");
            })
            .show();
    }

    @Override public void onBackPressed() {
        if (webView != null && webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }
}
