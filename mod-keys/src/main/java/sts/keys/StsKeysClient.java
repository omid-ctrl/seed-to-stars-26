package sts.keys;

import com.mojang.blaze3d.platform.InputConstants;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keymapping.v1.KeyMappingHelper;

import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.resources.Identifier;

public final class StsKeysClient implements ClientModInitializer {
	public static final String MOD_ID = "sts_keys";

	@Override
	public void onInitializeClient() {
		// Lang key: key.category.sts_keys.main
		KeyMapping.Category category = KeyMapping.Category.register(Identifier.fromNamespaceAndPath(MOD_ID, "main"));

		// 26.x key codes are SDL scancodes, so use InputConstants (GLFW_KEY_* values would map to other keys).
		KeyMapping toggleBars = register("toggle_bars", InputConstants.KEY_SEMICOLON, category);
		KeyMapping showProgress = register("show_progress", InputConstants.KEY_APOSTROPHE, category);
		KeyMapping bosses = register("bosses", InputConstants.KEY_LBRACKET, category);

		ClientTickEvents.END_CLIENT_TICK.register(client -> {
			sendOnPress(client, toggleBars, "trigger sts_bars");
			sendOnPress(client, showProgress, "trigger sts_status");
			sendOnPress(client, bosses, "trigger sts_bosses");
		});
	}

	private static KeyMapping register(String name, int defaultKey, KeyMapping.Category category) {
		return KeyMappingHelper.registerKeyMapping(
				new KeyMapping("key." + MOD_ID + "." + name, InputConstants.Type.KEYBOARD, defaultKey, category));
	}

	private static void sendOnPress(Minecraft client, KeyMapping key, String command) {
		while (key.consumeClick()) {
			LocalPlayer player = client.player;

			// Presses made outside a world are drained and dropped.
			if (player != null && client.level != null) {
				player.connection.sendCommand(command); // no leading slash
			}
		}
	}
}
