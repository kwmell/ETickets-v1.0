category_id = None
ticket_access_id = None
transcript_id = None

import os
import discord
import discord.ext.commands as commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
transcript_channel_id = None

@client.event
async def on_ready():
    try:
        print(f"[INFO] Client is up as {client.user}.")
        global transcript_channel_id
        transcript_channel_id = client.get_channel(transcript_id)

        if transcript_channel_id is None:
            print("[ERROR] Transcript channel not found. Make sure the channel ID is correct and the bot has access.")
        
        if not os.path.exists("transcripts"):
            print("[INFO] transcripts folder not found. Running setup.bat...")
            os.system("setup.bat")
    except Exception as e:
        print(f"[ERROR] {e}.")

@client.command(name="tickets")
async def tickets(ctx: commands.Context):
    try:
        await ctx.message.delete()

        embed = discord.Embed(
            title=f"{ctx.guild.name}: Tickets",
            description=f"Click the button below to open a ticket!",
            color=discord.Color.random()
        )

        embed.set_author(
            name="kwmell",
            icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
        )

        embed.set_footer(
            text="Made by kwmell",
            icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
        )

        view = discord.ui.View()

        view.add_item(discord.ui.Button(label=f"Open a Ticket", emoji="🎫", custom_id="open_a_ticket", style=discord.ButtonStyle.success))

        await ctx.send(view=view, embed=embed)

    except Exception as e:
        print(f"[ERROR] {e}.")

@client.event
async def on_interaction(inc: discord.Interaction):
    if inc.data["custom_id"] == "open_a_ticket":
        try:
            embed = discord.Embed(
                title=f"Wait...",
                description=f"Wait some seconds please!",
                color=discord.Color.red()
            )

            embed.set_author(
                name="kwmell",
                icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
            )

            embed.set_footer(
                text="Made by kwmell",
                icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
            )

            await inc.response.send_message(embed=embed, ephemeral=True)
            
            for channel in inc.guild.text_channels:
                if channel.topic == inc.user.id:
                    embed = discord.Embed(
                        title=f"Error",
                        description=f"You already have a ticket: {ch.mention}",
                        color=discord.Color.red()
                    )

                    embed.set_author(
                        name="kwmell",
                        icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
                    )

                    embed.set_footer(
                        text="Made by kwmell",
                        icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
                    )

                    await inc.edit_original_response(embed=embed, ephemeral=True)
                    return
                
            category = discord.utils.get(inc.guild.categories, id=category_id)
            ticketaccess = inc.guild.get_role(ticket_access_id)

            ow = {
                inc.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True, send_tts_messages=True),
                ticketaccess: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True, send_tts_messages=True),
                inc.guild.default_role: discord.PermissionOverwrite(view_channel=False)
            }

            ch = await category.create_text_channel(name=f"ticket-{inc.user.name}")

            await ch.edit(overwrites=ow, topic=str(inc.user.id))

            embed = discord.Embed(
                title=f"Thank you for opening a ticket!",
                description=f"Channel created here: {ch.mention}!",
                color=discord.Color.random()
            )

            embed.set_author(
                name="kwmell",
                icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
            )

            embed.set_footer(
                text="Made by kwmell",
                icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
            )

            await inc.edit_original_response(embed=embed, ephemeral=True)

            view = discord.ui.View()

            view.add_item(discord.ui.Button(label=f"Close", style=discord.ButtonStyle.danger, emoji="🔐", custom_id="close_a_ticket"))
            view.add_item(discord.ui.Button(label=f"Claim", style=discord.ButtonStyle.success, emoji="💕", custom_id="claim_a_ticket"))

            await ch.send(f"{ticketaccess.mention} {inc.user.mention}", embed=embed, view=view)
        except Exception as e:
            print(f"[ERROR] {e}.")
    elif inc.data["custom_id"] == "close_a_ticket":
        try:
            if inc.user.id == int(inc.channel.topic):
                embed = discord.Embed(
                    title=f"Are you sure?",
                    description=f"Do you wanna close your ticket?",
                    color=discord.Color.random()
                )

                view = discord.ui.View()

                view.add_item(discord.ui.Button(label=f"Confirm", emoji="✅", custom_id="close_a_ticket_confirm", style=discord.ButtonStyle.success))
                view.add_item(discord.ui.Button(label=f"Cancel", emoji="❌", custom_id="close_a_ticket_cancel", style=discord.ButtonStyle.danger))

                embed.set_author(
                    name="kwmell",
                    icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
                )

                embed.set_footer(
                    text="Made by kwmell",
                    icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
                )

                await inc.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            print(f"[ERROR] {e}.")
    elif inc.data["custom_id"] == "close_a_ticket_cancel":
        try:
            embed = discord.Embed(
                title=f"Done!",
                description=f"You cancelled the operation.",
                color=discord.Color.random()
            )

            embed.set_author(
                name="kwmell",
                icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
            )

            embed.set_footer(
                text="Made by kwmell",
                icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
            )

            view = discord.ui.View()
            await inc.response.edit_message(embed=embed, view=view)
        except Exception as e:
            print(f"[ERROR] {e}.")
    elif inc.data["custom_id"] == "close_a_ticket_confirm":
        try:
            embed = discord.Embed(
                title=f"Done!",
                description=f"Deleting ticket...",
                color=discord.Color.random()
            )

            embed.set_author(
                name="kwmell",
                icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
            )

            embed.set_footer(
                text="Made by kwmell",
                icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
            )

            await inc.response.send_message(embed=embed, ephemeral=True)

            transcript_content = ""

            async for message in inc.channel.history(limit=None):
                if message.content:
                    transcript_content += f"[{message.author.display_name} ({message.created_at.strftime('%Y-%m-%d %H:%M:%S')})]:> {message.content}\n"
                else:
                    continue

            transcript_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcripts", f"transcript_{inc.channel.name}.txt")

            with open(transcript_file, "w", encoding="utf-8") as file:
                file.write(transcript_content)

            transcript_embed = discord.Embed(
                title=f"TRANSCRIPT",
                description=f"- **Channel:** `{inc.channel.name}`.\n- **Closed by:** `{inc.user.name}#{inc.user.discriminator}`.",
                color=discord.Color.random()
            )
            transcript_embed.set_author(
                name="kwmell",
                icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
            )
            transcript_embed.set_footer(
                text="Made by kwmell",
                icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
            )

            with open(transcript_file, "r", encoding="utf-8") as file:
                await transcript_channel_id.send(embed=transcript_embed, file=discord.File(transcript_file))

            await inc.channel.delete()
        except Exception as e:
            print(f"[ERROR] {e}.")
    elif inc.data["custom_id"] == "claim_a_ticket":
        try:
            if inc.user.id == int(inc.channel.topic):
                embed = discord.Embed(
                    title=f"Uh oh!",
                    description=f"You can't claim your own ticket!",
                    color=discord.Color.random()
                )

                embed.set_author(
                    name="kwmell",
                    icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
                )

                embed.set_footer(
                    text="Made by kwmell",
                    icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
                )

                await inc.response.send_message(embed=embed, ephemeral=True)
            else:
                user = inc.guild.get_member(int(inc.channel.topic))

                ow = {
                    inc.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True, send_tts_messages=True),
                    user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True, send_tts_messages=True),
                    ticketaccess: discord.PermissionOverwrite(view_channel=False, send_messages=False, attach_files=False, embed_links=False, send_tts_messages=False),
                    inc.guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False, attach_files=False, embed_links=False, send_tts_messages=False)
                }

                embed = discord.Embed(
                    title=f"This ticket has been claimed!",
                    description=f"Claimed by {inc.user.mention}",
                    color=discord.Color.random()
                )

                embed.set_author(
                    name="kwmell",
                    icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
                )

                embed.set_footer(
                    text="Made by kwmell",
                    icon_url="https://cdn.discordapp.com/avatars/1171146705337593957/d414f0ce81e880e33568f07273cf4cbc.png?size=128"
                )

                view = discord.ui.View()

                view.add_item(discord.ui.Button(label=f"Close", style=discord.ButtonStyle.danger, emoji="🔐", custom_id="close_a_ticket"))

                await inc.response.edit_message(view=view)
                await inc.channel.send(embed=embed)
        except Exception as e:
            print(f"[ERROR] {e}.")

client.run("PUT-YOUR-TOKEN-HERE")
