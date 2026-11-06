package com.example.nsebreakout

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { MaterialTheme { ScannerHome() } }
    }
}

@Composable
fun ScannerHome() {
    var enabled by remember { mutableStateOf(false) }
    Scaffold { padding ->
        Column(Modifier.padding(padding).padding(20.dp).fillMaxSize()) {
            Text("NSE Breakout Alert Pro", style = MaterialTheme.typography.headlineSmall)
            Spacer(Modifier.height(8.dp))
            Text("Scanner status: " + if (enabled) "ON" else "OFF")
            Text("Scan interval: 5 minutes (backend scheduler required)")
            Spacer(Modifier.height(16.dp))
            Button(onClick = { enabled = !enabled }, modifier = Modifier.fillMaxWidth()) {
                Text(if (enabled) "STOP SCANNER" else "START SCANNER")
            }
            Spacer(Modifier.height(20.dp))
            Text("Alert feed", style = MaterialTheme.typography.titleMedium)
            Spacer(Modifier.height(8.dp))
            Text("No live alerts. Connect a licensed market-data provider to activate scanning.")
            Spacer(Modifier.height(20.dp))
            Text("Required filters", style = MaterialTheme.typography.titleMedium)
            LazyColumn {
                items(16) { i -> Text(
                    listOf(
                        "Daily close > 52-week-ago high",
                        "Daily close ≥ ₹100",
                        "Daily close > 99% of 250-day high",
                        "Daily volume > 6,000,000",
                        "Daily close > previous day's high",
                        "Daily close > EMA 20",
                        "EMA 20 > EMA 50 > SMA 200",
                        "Daily RSI(14): 62–75",
                        "Weekly RSI(14) > 65",
                        "Weekly close > weekly SMA(30)",
                        "Weekly SMA(30) rising vs 5 weeks ago",
                        "Custom indicator #3899, length 21 > 15.8",
                        "EMA 5 > EMA 10 > EMA 20",
                        "Daily MFI(14) > 72",
                        "Daily volume > previous day's volume",
                        "Daily CCI(20) ≥ 100"
                    )[i], modifier = Modifier.padding(vertical = 4.dp)
                ) }
            }
        }
    }
}
