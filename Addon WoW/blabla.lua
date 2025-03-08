local frame = CreateFrame("Frame") 
local text = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
text:SetPoint("RIGHT", UIParent, "RIGHT", -50, 0) -- Côté droit
text:SetFont("Fonts\\FRIZQT__.TTF", 12, "OUTLINE") -- 12 = Taille police

local lastLogTime = 0

local function WriteLog(message)
    if DEFAULT_CHAT_FRAME then
        DEFAULT_CHAT_FRAME:AddMessage("|cff66ccff[SPECTRE]|r " .. message)
    end
end

frame:SetScript("OnUpdate", function()
    local hp = UnitHealth("player")
    local maxHp = UnitHealthMax("player")
    local mana = UnitMana("player")
    local maxMana = UnitManaMax("player")
    local currentTime = GetTime()

    -- Position Map (2D uniquement Turtle WoW)
    local x, y = GetPlayerMapPosition("player")

    local targetName = "Aucune cible"
    local targetLevel = "N/A"
    local targetFriendly = "N/A"
    local targetHp = "N/A"
    local targetMaxHp = "N/A"

    if UnitExists("target") then
        targetName = UnitName("target") or "Inconnu"
        targetLevel = UnitLevel("target") or "N/A"
        targetFriendly = UnitIsFriend("player", "target") and "Amical" or "Ennemi"
        targetHp = UnitHealth("target") or "N/A"
        targetMaxHp = UnitHealthMax("target") or "N/A"
    end

    local color = "|cff66ccff"  -- Bleu clair pour les infos
    local displayText = color .. "HP: " .. hp .. "/" .. maxHp .. "|r"

    if maxMana > 0 then
        displayText = displayText .. "   " .. color .. "Mana: " .. mana .. "/" .. maxMana .. "|r"
    end

    displayText = displayText .. "\n|cffffff00Pos: X=" .. string.format("%.3f", x) .. " Y=" .. string.format("%.3f", y) .. "|r"

    if UnitExists("target") then
        displayText = displayText .. "\n" .. color .. "Target: " .. targetName .. " (Level " .. targetLevel .. ") - " .. targetFriendly .. "|r"
        displayText = displayText .. "\n" .. color .. "Target Vie: " .. targetHp .. "/" .. targetMaxHp .. "|r"
    end

    text:SetText(displayText)

    -- Log toutes les 2 secondes
    if currentTime - lastLogTime >= 2 then
        WriteLog("HP: " .. hp .. "/" .. maxHp .. " | Mana: " .. mana .. "/" .. maxMana .. " | Pos: X=" .. string.format("%.3f", x) .. " Y=" .. string.format("%.3f", y))
        if UnitExists("target") then
            WriteLog("Target: " .. targetName .. " (Level " .. targetLevel .. ") - " .. targetFriendly)
            WriteLog("Target Vie: " .. targetHp .. "/" .. targetMaxHp)
        end
        lastLogTime = currentTime
    end
end)
